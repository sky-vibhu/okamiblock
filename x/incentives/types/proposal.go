package types

import (
	"errors"

	govcdc "github.com/cosmos/cosmos-sdk/x/gov/codec"
	govv1beta1 "github.com/cosmos/cosmos-sdk/x/gov/types/v1beta1"
	okamitypes "github.com/okamiblock/okamiblock/types"
)

// constants
const (
	ProposalTypeRegisterIncentive string = "RegisterIncentive"
	ProposalTypeCancelIncentive   string = "CancelIncentive"
)

// Implements Proposal Interface
var (
	_ govv1beta1.Content = &RegisterIncentiveProposal{}
	_ govv1beta1.Content = &CancelIncentiveProposal{}
)

func init() {
	govv1beta1.RegisterProposalType(ProposalTypeRegisterIncentive)
	govv1beta1.RegisterProposalType(ProposalTypeCancelIncentive)
	govcdc.ModuleCdc.Amino.RegisterConcrete(&RegisterIncentiveProposal{}, "incentives/RegisterIncentiveProposal", nil)
	govcdc.ModuleCdc.Amino.RegisterConcrete(&CancelIncentiveProposal{}, "incentives/CancelIncentiveProposal", nil)
}

// ProposalRoute returns router key for this proposal
func (*RegisterIncentiveProposal) ProposalRoute() string { return RouterKey }

// ProposalType returns proposal type for this proposal
func (*RegisterIncentiveProposal) ProposalType() string {
	return ProposalTypeRegisterIncentive
}

// ValidateBasic performs a stateless check of the proposal fields
func (rip *RegisterIncentiveProposal) ValidateBasic() error {
	return errors.New("Deprecated")
}

// ProposalRoute returns router key for this proposal
func (*CancelIncentiveProposal) ProposalRoute() string { return RouterKey }

// ProposalType returns proposal type for this proposal
func (*CancelIncentiveProposal) ProposalType() string {
	return ProposalTypeCancelIncentive
}

// ValidateBasic performs a stateless check of the proposal fields
func (rip *CancelIncentiveProposal) ValidateBasic() error {
	if err := okamitypes.ValidateAddress(rip.Contract); err != nil {
		return err
	}
	return errors.New("Deprecated")
}
