package app

import (
	sdk "github.com/cosmos/cosmos-sdk/types"

	"github.com/okamiblock/okamiblock/utils"
)

// ScheduleForkUpgrade executes any necessary fork logic for based upon the current
// block height and chain ID (mainnet or testnet). It sets an upgrade plan once
// the chain reaches the pre-defined upgrade height.
//
// CONTRACT: for this logic to work properly it is required to:
//
//  1. Release a non-breaking patch version so that the chain can set the scheduled upgrade plan at upgrade-height.
//  2. Release the software defined in the upgrade-info
func (app *Okami) ScheduleForkUpgrade(ctx sdk.Context) {
	// Only fork on Mainnet
	if !utils.IsMainnet(ctx.ChainID()) {
		return
	}
	// handle mainnet forks with their corresponding upgrade name and info
	switch ctx.BlockHeight() {
	default:
		// No-op
		return
	}

}
