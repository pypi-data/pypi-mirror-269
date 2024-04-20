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

use std::fmt::{Display, Formatter};

use derive_builder::Builder;
use nautilus_core::{nanos::UnixNanos, uuid::UUID4};
use serde::{Deserialize, Serialize};

use crate::identifiers::{
    client_order_id::ClientOrderId, instrument_id::InstrumentId, strategy_id::StrategyId,
    trader_id::TraderId,
};

#[repr(C)]
#[derive(Clone, Copy, PartialEq, Eq, Debug, Default, Serialize, Deserialize, Builder)]
#[builder(default)]
#[serde(tag = "type")]
#[cfg_attr(
    feature = "python",
    pyo3::pyclass(module = "nautilus_trader.core.nautilus_pyo3.model")
)]
pub struct OrderEmulated {
    pub trader_id: TraderId,
    pub strategy_id: StrategyId,
    pub instrument_id: InstrumentId,
    pub client_order_id: ClientOrderId,
    pub event_id: UUID4,
    pub ts_event: UnixNanos,
    pub ts_init: UnixNanos,
}

impl OrderEmulated {
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        trader_id: TraderId,
        strategy_id: StrategyId,
        instrument_id: InstrumentId,
        client_order_id: ClientOrderId,
        event_id: UUID4,
        ts_event: UnixNanos,
        ts_init: UnixNanos,
    ) -> anyhow::Result<Self> {
        Ok(Self {
            trader_id,
            strategy_id,
            instrument_id,
            client_order_id,
            event_id,
            ts_event,
            ts_init,
        })
    }
}

impl Display for OrderEmulated {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "OrderEmulated(instrument_id={}, client_order_id={})",
            self.instrument_id, self.client_order_id
        )
    }
}

////////////////////////////////////////////////////////////////////////////////
// Tests
////////////////////////////////////////////////////////////////////////////////
#[cfg(test)]
mod tests {
    use rstest::rstest;

    use crate::events::order::{emulated::OrderEmulated, stubs::*};

    #[rstest]
    fn test_order_emulated(order_emulated: OrderEmulated) {
        let display = format!("{order_emulated}");
        assert_eq!(
            display,
            "OrderEmulated(instrument_id=BTCUSDT.COINBASE, client_order_id=O-20200814-102234-001-001-1)"
        );
    }
}
