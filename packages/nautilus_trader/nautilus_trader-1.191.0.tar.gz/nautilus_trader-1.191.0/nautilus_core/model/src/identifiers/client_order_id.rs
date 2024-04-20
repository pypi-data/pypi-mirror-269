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

use std::{
    fmt::{Debug, Display, Formatter},
    hash::Hash,
};

use nautilus_core::correctness::check_valid_string;
use ustr::Ustr;

/// Represents a valid client order ID (assigned by the Nautilus system).
#[repr(C)]
#[derive(Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
#[cfg_attr(
    feature = "python",
    pyo3::pyclass(module = "nautilus_trader.core.nautilus_pyo3.model")
)]
pub struct ClientOrderId(Ustr);

impl ClientOrderId {
    /// Creates a new `ClientOrderId` instance from the given identifier value.
    ///
    /// # Panics
    ///
    /// Panics if the value is not a valid string.
    pub fn new(value: &str) -> anyhow::Result<Self> {
        check_valid_string(value, stringify!(value))?;

        Ok(Self(Ustr::from(value)))
    }

    /// Sets the inner identifier value.
    pub(crate) fn set_inner(&mut self, value: &str) {
        self.0 = Ustr::from(value);
    }

    /// Returns the inner identifier value.
    pub fn inner(&self) -> Ustr {
        self.0
    }

    /// Returns the inner identifier value as a string slice.
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

impl Default for ClientOrderId {
    fn default() -> Self {
        // SAFETY: Default value is safe
        Self::new("O-123456789").unwrap()
    }
}

impl Debug for ClientOrderId {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.0)
    }
}

impl Display for ClientOrderId {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

#[must_use]
pub fn optional_ustr_to_vec_client_order_ids(s: Option<Ustr>) -> Option<Vec<ClientOrderId>> {
    s.map(|ustr| {
        let s_str = ustr.to_string();
        s_str
            .split(',')
            .map(|s| ClientOrderId::new(s).unwrap())
            .collect::<Vec<ClientOrderId>>()
    })
}

#[must_use]
pub fn optional_vec_client_order_ids_to_ustr(vec: Option<Vec<ClientOrderId>>) -> Option<Ustr> {
    vec.map(|client_order_ids| {
        let s: String = client_order_ids
            .into_iter()
            .map(|id| id.to_string())
            .collect::<Vec<String>>()
            .join(",");
        Ustr::from(&s)
    })
}

impl From<&str> for ClientOrderId {
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
    use ustr::Ustr;

    use super::ClientOrderId;
    use crate::identifiers::{
        client_order_id::{
            optional_ustr_to_vec_client_order_ids, optional_vec_client_order_ids_to_ustr,
        },
        stubs::*,
    };

    #[rstest]
    fn test_string_reprs(client_order_id: ClientOrderId) {
        assert_eq!(client_order_id.as_str(), "O-20200814-102234-001-001-1");
        assert_eq!(format!("{client_order_id}"), "O-20200814-102234-001-001-1");
    }

    #[rstest]
    fn test_optional_ustr_to_vec_client_order_ids() {
        // Test with None
        assert_eq!(optional_ustr_to_vec_client_order_ids(None), None);

        // Test with Some
        let ustr = Ustr::from("id1,id2,id3");
        let client_order_ids = optional_ustr_to_vec_client_order_ids(Some(ustr)).unwrap();
        assert_eq!(client_order_ids[0].as_str(), "id1");
        assert_eq!(client_order_ids[1].as_str(), "id2");
        assert_eq!(client_order_ids[2].as_str(), "id3");
    }

    #[rstest]
    fn test_optional_vec_client_order_ids_to_ustr() {
        // Test with None
        assert_eq!(optional_vec_client_order_ids_to_ustr(None), None);

        // Test with Some
        let client_order_ids = vec![
            ClientOrderId::from("id1"),
            ClientOrderId::from("id2"),
            ClientOrderId::from("id3"),
        ];
        let ustr = optional_vec_client_order_ids_to_ustr(Some(client_order_ids)).unwrap();
        assert_eq!(ustr.to_string(), "id1,id2,id3");
    }
}
