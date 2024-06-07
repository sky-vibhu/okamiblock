package types

import (
	"math/big"

	sdkmath "cosmossdk.io/math"

	sdk "github.com/cosmos/cosmos-sdk/types"
)

const (
	// AttoOkami defines the default coin denomination used in Okami in:
	//
	// - Staking parameters: denomination used as stake in the dPoS chain
	// - Mint parameters: denomination minted due to fee distribution rewards
	// - Governance parameters: denomination used for spam prevention in proposal deposits
	// - Crisis parameters: constant fee denomination used for spam prevention to check broken invariant
	// - EVM parameters: denomination used for running EVM state transitions in Okami.
	AttoOkami string = "aOKM"

	// BaseDenomUnit defines the base denomination unit for Okami.
	// 1 okami = 1x10^{BaseDenomUnit} aOKM
	BaseDenomUnit = 18

	// DefaultGasPrice is default gas price for evm transactions
	DefaultGasPrice = 20
)

// PowerReduction defines the default power reduction value for staking
var PowerReduction = sdkmath.NewIntFromBigInt(new(big.Int).Exp(big.NewInt(10), big.NewInt(BaseDenomUnit), nil))

// NewOkamiCoin is a utility function that returns an "aOKM" coin with the given sdkmath.Int amount.
// The function will panic if the provided amount is negative.
func NewOkamiCoin(amount sdkmath.Int) sdk.Coin {
	return sdk.NewCoin(AttoOkami, amount)
}

// NewOkamiDecCoin is a utility function that returns an "aOKM" decimal coin with the given sdkmath.Int amount.
// The function will panic if the provided amount is negative.
func NewOkamiDecCoin(amount sdkmath.Int) sdk.DecCoin {
	return sdk.NewDecCoin(AttoOkami, amount)
}

// NewOkamiCoinInt64 is a utility function that returns an "aOKM" coin with the given int64 amount.
// The function will panic if the provided amount is negative.
func NewOkamiCoinInt64(amount int64) sdk.Coin {
	return sdk.NewInt64Coin(AttoOkami, amount)
}
