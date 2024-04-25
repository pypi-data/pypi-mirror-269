use crate::fixer::{Fixer, FixerError, SerializableFixer};
use crate::rule::referent_rule::RuleRegistration;
use crate::rule::Rule;
use crate::rule::{RuleSerializeError, SerializableRule};
use crate::transform::{apply_env_transform, Transformation};
use crate::DeserializeEnv;

use ast_grep_core::language::Language;
use ast_grep_core::meta_var::MetaVarEnv;
use ast_grep_core::{Doc, Matcher, Node};
use serde::{Deserialize, Serialize};
use serde_yaml::Error as YamlError;

use bit_set::BitSet;
use schemars::JsonSchema;
use thiserror::Error;

use std::borrow::Cow;
use std::collections::{HashMap, HashSet};
use std::ops::Deref;

#[derive(Debug, Error)]
pub enum RuleConfigError {
  #[error("Fail to parse yaml as RuleConfig")]
  Yaml(#[from] YamlError),
  #[error("Rule is not configured correctly.")]
  Rule(#[from] RuleSerializeError),
  #[error("Utility rule is not configured correctly.")]
  Utils(#[source] RuleSerializeError),
  #[error("fix pattern is invalid.")]
  Fixer(#[from] FixerError),
  #[error("constraints is not configured correctly.")]
  Constraints(#[source] RuleSerializeError),
  #[error("Undefined meta var {0} used in {1}.")]
  UndefinedMetaVar(String, &'static str),
  #[error("Undefined rewriter {0} used in transform.")]
  UndefinedRewriter(String),
}

type RResult<T> = std::result::Result<T, RuleConfigError>;

/// Used for global rules, rewriters, and pyo3/napi
#[derive(Serialize, Deserialize, Clone, JsonSchema)]
pub struct SerializableRuleCore {
  /// A rule object to find matching AST nodes
  pub rule: SerializableRule,
  /// Additional meta variables pattern to filter matching
  pub constraints: Option<HashMap<String, SerializableRule>>,
  /// Utility rules that can be used in `matches`
  pub utils: Option<HashMap<String, SerializableRule>>,
  /// A dictionary for metavariable manipulation. Dict key is the new variable name.
  /// Dict value is a [transformation] that specifies how meta var is processed.
  /// See [transformation doc](https://ast-grep.github.io/reference/yaml/transformation.html).
  pub transform: Option<HashMap<String, Transformation>>,
  /// A pattern string or a FixConfig object to auto fix the issue.
  /// It can reference metavariables appeared in rule.
  /// See details in fix [object reference](https://ast-grep.github.io/reference/yaml/fix.html#fixconfig).
  pub fix: Option<SerializableFixer>,
}

impl SerializableRuleCore {
  pub(crate) fn get_deserialize_env<L: Language>(
    &self,
    env: DeserializeEnv<L>,
  ) -> RResult<DeserializeEnv<L>> {
    if let Some(utils) = &self.utils {
      let env = env
        .register_local_utils(utils)
        .map_err(RuleConfigError::Rule)?;
      Ok(env)
    } else {
      Ok(env)
    }
  }

  fn get_constraints<L: Language>(
    &self,
    env: &DeserializeEnv<L>,
  ) -> RResult<HashMap<String, Rule<L>>> {
    let mut matchers = HashMap::new();
    let Some(constraints) = &self.constraints else {
      return Ok(matchers);
    };
    for (key, ser) in constraints {
      matchers.insert(key.to_string(), env.deserialize_rule(ser.clone())?);
    }
    Ok(matchers)
  }

  fn get_fixer<L: Language>(&self, env: &DeserializeEnv<L>) -> RResult<Option<Fixer<L>>> {
    if let Some(fix) = &self.fix {
      let parsed = Fixer::parse(fix, env, &self.transform)?;
      Ok(Some(parsed))
    } else {
      Ok(None)
    }
  }

  fn get_matcher_from_env<L: Language>(&self, env: &DeserializeEnv<L>) -> RResult<RuleCore<L>> {
    let rule = env.deserialize_rule(self.rule.clone())?;
    let matchers = self.get_constraints(env)?;
    let vars = Self::check_var_in_constraints(&rule, &matchers)?;
    let vars = Self::check_var_in_transform(vars, &self.transform)?;
    let transform = self.transform.clone();
    let fixer = self.get_fixer(env)?;
    Self::check_var_in_fix(vars, &fixer)?;
    Ok(
      RuleCore::new(rule)
        .with_matchers(matchers)
        .with_utils(env.registration.clone())
        .with_transform(transform)
        .with_fixer(fixer),
    )
  }

  fn check_var_in_constraints<'r, L: Language>(
    rule: &'r Rule<L>,
    constraints: &'r HashMap<String, Rule<L>>,
  ) -> RResult<HashSet<&'r str>> {
    let mut vars = rule.defined_vars();
    for rule in constraints.values() {
      for var in rule.defined_vars() {
        vars.insert(var);
      }
    }
    for var in constraints.keys() {
      let var: &str = var;
      if !vars.contains(var) {
        return Err(RuleConfigError::UndefinedMetaVar(
          var.to_owned(),
          "constraints",
        ));
      }
    }
    Ok(vars)
  }

  fn check_var_in_transform<'r>(
    mut vars: HashSet<&'r str>,
    transform: &'r Option<HashMap<String, Transformation>>,
  ) -> RResult<HashSet<&'r str>> {
    let Some(transform) = transform else {
      return Ok(vars);
    };
    for var in transform.keys() {
      vars.insert(var);
    }
    for trans in transform.values() {
      let needed = trans.used_vars();
      if !vars.contains(needed) {
        return Err(RuleConfigError::UndefinedMetaVar(
          needed.to_string(),
          "transform",
        ));
      }
    }
    Ok(vars)
  }

  fn check_var_in_fix<L: Language>(vars: HashSet<&str>, fixer: &Option<Fixer<L>>) -> RResult<()> {
    let Some(fixer) = fixer else {
      return Ok(());
    };
    for var in fixer.used_vars() {
      if !vars.contains(&var) {
        return Err(RuleConfigError::UndefinedMetaVar(var.to_string(), "fix"));
      }
    }
    Ok(())
  }

  pub fn get_matcher<L: Language>(&self, env: DeserializeEnv<L>) -> RResult<RuleCore<L>> {
    let env = self.get_deserialize_env(env)?;
    self.get_matcher_from_env(&env)
  }
}

pub struct RuleCore<L: Language> {
  rule: Rule<L>,
  matchers: HashMap<String, Rule<L>>,
  kinds: Option<BitSet>,
  pub(crate) transform: Option<HashMap<String, Transformation>>,
  pub fixer: Option<Fixer<L>>,
  // this is required to hold util rule reference
  utils: RuleRegistration<L>,
}

impl<L: Language> RuleCore<L> {
  #[inline]
  pub fn new(rule: Rule<L>) -> Self {
    let kinds = rule.potential_kinds();
    Self {
      rule,
      kinds,
      ..Default::default()
    }
  }

  #[inline]
  pub fn with_matchers(self, matchers: HashMap<String, Rule<L>>) -> Self {
    Self { matchers, ..self }
  }

  #[inline]
  pub fn with_utils(self, utils: RuleRegistration<L>) -> Self {
    Self { utils, ..self }
  }

  #[inline]
  pub fn with_transform(self, transform: Option<HashMap<String, Transformation>>) -> Self {
    Self { transform, ..self }
  }

  #[inline]
  pub fn with_fixer(self, fixer: Option<Fixer<L>>) -> Self {
    Self { fixer, ..self }
  }

  pub fn get_env(&self, lang: L) -> DeserializeEnv<L> {
    DeserializeEnv {
      lang,
      registration: self.utils.clone(),
    }
  }

  pub fn defined_vars(&self) -> HashSet<&str> {
    let mut ret = self.rule.defined_vars();
    for v in self.utils.get_local_util_vars() {
      ret.insert(v);
    }
    for constraint in self.matchers.values() {
      for var in constraint.defined_vars() {
        ret.insert(var);
      }
    }
    if let Some(trans) = &self.transform {
      for key in trans.keys() {
        ret.insert(key);
      }
    }
    ret
  }
}
impl<L: Language> Deref for RuleCore<L> {
  type Target = Rule<L>;
  fn deref(&self) -> &Self::Target {
    &self.rule
  }
}

impl<L: Language> Default for RuleCore<L> {
  #[inline]
  fn default() -> Self {
    Self {
      rule: Rule::default(),
      matchers: HashMap::default(),
      kinds: None,
      transform: None,
      fixer: None,
      utils: RuleRegistration::default(),
    }
  }
}

impl<L: Language> Matcher<L> for RuleCore<L> {
  fn match_node_with_env<'tree, D: Doc<Lang = L>>(
    &self,
    node: Node<'tree, D>,
    env: &mut Cow<MetaVarEnv<'tree, D>>,
  ) -> Option<Node<'tree, D>> {
    if let Some(kinds) = &self.kinds {
      if !kinds.contains(node.kind_id().into()) {
        return None;
      }
    }
    let ret = self.rule.match_node_with_env(node, env)?;
    if !env.to_mut().match_constraints(&self.matchers) {
      return None;
    }
    if let Some(trans) = &self.transform {
      let lang = ret.lang();
      let rewriters = self.utils.get_rewriters();
      apply_env_transform(trans, lang, env.to_mut(), rewriters);
    }
    Some(ret)
  }

  fn potential_kinds(&self) -> Option<BitSet> {
    self.rule.potential_kinds()
  }
}

#[cfg(test)]
mod test {
  use super::*;
  use crate::rule::referent_rule::ReferentRule;
  use crate::test::TypeScript;
  use crate::{from_str, GlobalRules};
  use ast_grep_core::matcher::{Pattern, RegexMatcher};

  #[test]
  fn test_rule_reg_with_utils() {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore =
      from_str("{rule: {matches: test}, utils: {test: {kind: number}} }").expect("should deser");
    let rule = ReferentRule::try_new("test".into(), &env.registration).expect("should work");
    let not = ReferentRule::try_new("test2".into(), &env.registration).expect("should work");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    let grep = TypeScript::Tsx.ast_grep("a = 123");
    assert!(grep.root().find(&matcher).is_some());
    assert!(grep.root().find(&rule).is_some());
    assert!(grep.root().find(&not).is_none());
    let grep = TypeScript::Tsx.ast_grep("a = '123'");
    assert!(grep.root().find(&matcher).is_none());
    assert!(grep.root().find(&rule).is_none());
    assert!(grep.root().find(&not).is_none());
  }

  #[test]
  fn test_rule_with_constraints() {
    let mut matchers = HashMap::new();
    matchers.insert(
      "A".to_string(),
      Rule::Regex(RegexMatcher::try_new("a").unwrap()),
    );
    let rule =
      RuleCore::new(Rule::Pattern(Pattern::new("$A", TypeScript::Tsx))).with_matchers(matchers);
    let grep = TypeScript::Tsx.ast_grep("a");
    assert!(grep.root().find(&rule).is_some());
    let grep = TypeScript::Tsx.ast_grep("bbb");
    assert!(grep.root().find(&rule).is_none());
  }

  #[test]
  fn test_constraints_inheriting_env() {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore =
      from_str("{rule: {pattern: $A = $B}, constraints: {A: {pattern: $B}} }")
        .expect("should deser");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    let grep = TypeScript::Tsx.ast_grep("a = a");
    assert!(grep.root().find(&matcher).is_some());
    let grep = TypeScript::Tsx.ast_grep("a = b");
    assert!(grep.root().find(&matcher).is_none());
  }

  #[test]
  fn test_constraints_writing_to_env() {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore =
      from_str("{rule: {pattern: $A = $B}, constraints: {B: {pattern: $C + $D}} }")
        .expect("should deser");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    let grep = TypeScript::Tsx.ast_grep("a = a");
    assert!(grep.root().find(&matcher).is_none());
    let grep = TypeScript::Tsx.ast_grep("a = 1 + 2");
    let nm = grep.root().find(&matcher).expect("should match");
    let env = nm.get_env();
    let matched = env.get_match("C").expect("should match C").text();
    assert_eq!(matched, "1");
    let matched = env.get_match("D").expect("should match D").text();
    assert_eq!(matched, "2");
  }

  fn get_rewriters() -> GlobalRules<TypeScript> {
    // NOTE: initialize a DeserializeEnv here is not 100% correct
    // it does not inherit global rules or local rules
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ret = GlobalRules::default();
    let rewriter: SerializableRuleCore =
      from_str("{rule: {kind: number, pattern: $REWRITE}, fix: yjsnp}").expect("should parse");
    let rewriter = rewriter.get_matcher(env).expect("should work");
    ret.insert("re", rewriter).expect("should work");
    ret
  }

  #[test]
  fn test_rewriter_writing_to_env() {
    let rewriters = get_rewriters();
    let env = DeserializeEnv::new(TypeScript::Tsx).with_rewriters(&rewriters);
    let ser_rule: SerializableRuleCore = from_str(
      r"
rule: {pattern: $A = $B}
transform:
  C:
    rewrite:
      source: $B
      rewriters: [re]",
    )
    .expect("should deser");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    let grep = TypeScript::Tsx.ast_grep("a = 1 + 2");
    let nm = grep.root().find(&matcher).expect("should match");
    let env = nm.get_env();
    let matched = env.get_match("B").expect("should match").text();
    assert_eq!(matched, "1 + 2");
    let matched = env.get_match("A").expect("should match").text();
    assert_eq!(matched, "a");
    let transformed = env.get_transformed("C").expect("should transform");
    assert_eq!(String::from_utf8_lossy(transformed), "yjsnp + yjsnp");
    assert!(env.get_match("REWRITE").is_none());

    let grep = TypeScript::Tsx.ast_grep("a = a");
    let nm = grep.root().find(&matcher).expect("should match");
    let env = nm.get_env();
    let matched = env.get_match("B").expect("should match").text();
    assert_eq!(matched, "a");
    let transformed = env.get_transformed("C").expect("should transform");
    assert_eq!(String::from_utf8_lossy(transformed), "a");
  }

  #[test]
  fn test_defined_vars() {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore = from_str(
      r"
rule: {pattern: $A = $B}
constraints:
  A: { pattern: $C = $D }
transform:
  E:
    substring:
      source: $B
      startCar: 1",
    )
    .expect("should deser");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    assert_eq!(
      matcher.defined_vars(),
      ["A", "B", "C", "D", "E"].into_iter().collect()
    );
  }

  fn get_undefined(src: &str) -> (String, &str) {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore = from_str(src).expect("should deser");
    match ser_rule.get_matcher(env) {
      Err(RuleConfigError::UndefinedMetaVar(name, section)) => (name, section),
      _ => panic!("should error"),
    }
  }

  #[test]
  fn test_undefined_vars_in_constraints() {
    let (name, section) = get_undefined(
      r"
rule: {pattern: $A}
constraints: {B: {pattern: bbb}}
",
    );
    assert_eq!(name, "B");
    assert_eq!(section, "constraints");
  }
  #[test]
  fn test_undefined_vars_in_transform() {
    let (name, section) = get_undefined(
      r"
rule: {pattern: $A}
constraints: {A: {pattern: $C}}
transform:
  B:
    replace: {source: $C, replace: a, by: b }
  D:
    replace: {source: $E, replace: a, by: b }
",
    );
    assert_eq!(name, "E");
    assert_eq!(section, "transform");
  }
  #[test]
  fn test_undefined_vars_in_fix() {
    let (name, section) = get_undefined(
      r"
rule: {pattern: $A}
constraints: {A: {pattern: $C}}
transform:
  B:
    replace: {source: $C, replace: a, by: b }
fix: $D
",
    );
    assert_eq!(name, "D");
    assert_eq!(section, "fix");
  }

  #[test]
  fn test_defined_vars_in_utils() {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore = from_str(
      r"
rule: {matches: test}
utils:
  test: { pattern: $B}",
    )
    .expect("should deser");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    assert_eq!(matcher.defined_vars(), ["B"].into_iter().collect());
  }

  #[test]
  fn test_defined_vars_cyclic() {
    let env = DeserializeEnv::new(TypeScript::Tsx);
    let ser_rule: SerializableRuleCore = from_str(
      r"
rule: { matches: test1 }
utils:
  test1: { pattern: $B, inside: {matches: test2} }
  test2: { pattern: $A, has: {matches: test1} }",
    )
    .expect("should deser");
    let matcher = ser_rule.get_matcher(env).expect("should parse");
    assert_eq!(matcher.defined_vars(), ["A", "B"].into_iter().collect());
  }
}
