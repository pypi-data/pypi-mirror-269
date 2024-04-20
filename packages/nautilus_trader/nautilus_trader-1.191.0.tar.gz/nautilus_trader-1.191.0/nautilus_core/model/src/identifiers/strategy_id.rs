// -------------------------------------------------------------------------------------------------
//  Copyright (C) 2015-2024 Nautech Systems Pty Ltd. All rights reserved.
//  https://nautechsystems.io
//
//  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
//  You may not use this file except in compliance with the License.
//  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
// -------------------------------------------------------------------------------------------------

use std::fmt::{Debug, Display, Formatter};

use nautilus_core::correctness::{check_string_contains, check_valid_string};
use ustr::Ustr;

/// The identifier for all 'external' strategy IDs (not local to this system instance).
const EXTERNAL_STRATEGY_ID: &str = "EXTERNAL";

/// Represents a valid strategy ID.
///
/// Must be correctly formatted with two valid strings either side of a hyphen.
/// It is expected a strategy ID is the class name of the strategy,
/// with an order ID tag number separated by a hyphen.
///
/// Example: "EMACross-001".
///
/// The reason for the numerical component of the ID is so that order and position IDs
/// do not collide with those from another strategy within the node instance.
#[repr(C)]
#[derive(Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
#[cfg_attr(
    feature = "python",
    pyo3::pyclass(module = "nautilus_trader.core.nautilus_pyo3.model")
)]
pub struct StrategyId(Ustr);

impl StrategyId {
    /// Creates a new `StrategyId` instance from the given identifier value.
    ///
    /// # Panics
    ///
    /// Panics if the value is not a valid string, or does not contain a hyphen '-' separator.
    pub fn new(value: &str) -> anyhow::Result<Self> {
        check_valid_string(value, stringify!(value))?;
        if value != EXTERNAL_STRATEGY_ID {
            check_string_contains(value, "-", stringify!(value))?;
        }

        Ok(Self(Ustr::from(value)))
    }

    /// Sets the inner identifier value.
    pub(crate) fn set_inner(&mut self, value: &str) {
        self.0 = Ustr::from(value);
    }

    /// Returns the inner identifier value.
    #[must_use]
    pub fn inner(&self) -> Ustr {
        self.0
    }

    /// Returns the inner identifier value as a string slice.
    #[must_use]
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }

    #[must_use]
    pub fn external() -> Self {
        // SAFETY:: Constant value is safe
        Self::new(EXTERNAL_STRATEGY_ID).unwrap()
    }

    #[must_use]
    pub fn is_external(&self) -> bool {
        self.0 == EXTERNAL_STRATEGY_ID
    }

    #[must_use]
    pub fn get_tag(&self) -> &str {
        // SAFETY: Unwrap safe as value previously validated
        self.0.split('-').last().unwrap()
    }
}

impl Default for StrategyId {
    fn default() -> Self {
        // SAFETY: Default value is safe
        Self::new("S-001").unwrap()
    }
}

impl Debug for StrategyId {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.0)
    }
}

impl Display for StrategyId {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl From<&str> for StrategyId {
    fn from(input: &str) -> Self {
        Self::new(input).unwrap()
    }
}

////////////////////////////////////////////////////////////////////////////////
// Tests
////////////////////////////////////////////////////////////////////////////////
#[cfg(test)]
mod tests {
    use rstest::rstest;

    use super::StrategyId;
    use crate::identifiers::stubs::*;

    #[rstest]
    fn test_string_reprs(strategy_id_ema_cross: StrategyId) {
        assert_eq!(strategy_id_ema_cross.as_str(), "EMACross-001");
        assert_eq!(format!("{strategy_id_ema_cross}"), "EMACross-001");
    }

    #[rstest]
    fn test_get_external() {
        assert_eq!(StrategyId::external().as_str(), "EXTERNAL");
    }

    #[rstest]
    fn test_is_external() {
        assert!(StrategyId::external().is_external());
    }

    #[rstest]
    fn test_get_tag(strategy_id_ema_cross: StrategyId) {
        assert_eq!(strategy_id_ema_cross.get_tag(), "001");
    }
}
