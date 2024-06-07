package grpc

import (
	sdktypes "github.com/cosmos/cosmos-sdk/types"
	authtypes "github.com/cosmos/cosmos-sdk/x/auth/types"
	banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
	"github.com/ethereum/go-ethereum/common"
	"github.com/okamiblock/okamiblock/testutil/integration/network"
	evmtypes "github.com/okamiblock/okamiblock/x/evm/types"
	feemarkettypes "github.com/okamiblock/okamiblock/x/feemarket/types"
)

// Handler is an interface that defines the methods that are used to query
// the network's modules via gRPC.
type Handler interface {
	// EVM methods
	GetEvmAccount(address common.Address) (*evmtypes.QueryAccountResponse, error)
	EstimateGas(args []byte, GasCap uint64) (*evmtypes.EstimateGasResponse, error)
	GetEvmParams() (*evmtypes.QueryParamsResponse, error)

	// Bank methods
	GetBalance(address sdktypes.AccAddress, denom string) (*banktypes.QueryBalanceResponse, error)

	// Account methods
	GetAccount(address string) (authtypes.AccountI, error)

	// FeeMarket methods
	GetBaseFee() (*feemarkettypes.QueryBaseFeeResponse, error)
}

var _ Handler = (*IntegrationHandler)(nil)

// IntegrationHandler is a helper struct to query the network's modules
// via gRPC. This is to simulate the behavior of a real user and avoid querying
// the modules directly.
type IntegrationHandler struct {
	network network.Network
}

// NewIntegrationHandler creates a new IntegrationHandler instance.
func NewIntegrationHandler(network network.Network) Handler {
	return &IntegrationHandler{
		network: network,
	}
}
