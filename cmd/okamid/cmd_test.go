package main_test

import (
	"fmt"
	"testing"

	"github.com/cosmos/cosmos-sdk/client/flags"
	svrcmd "github.com/cosmos/cosmos-sdk/server/cmd"
	"github.com/cosmos/cosmos-sdk/x/genutil/client/cli"
	"github.com/stretchr/testify/require"

	"github.com/okamiblock/okamiblock/app"
	okamid "github.com/okamiblock/okamiblock/cmd/okamid"
	"github.com/okamiblock/okamiblock/utils"
)

func TestInitCmd(t *testing.T) {
	rootCmd, _ := okamid.NewRootCmd()
	rootCmd.SetArgs([]string{
		"init",       // Test the init cmd
		"okami-test", // Moniker
		fmt.Sprintf("--%s=%s", cli.FlagOverwrite, "true"), // Overwrite genesis.json, in case it already exists
		fmt.Sprintf("--%s=%s", flags.FlagChainID, utils.TestnetChainID+"-1"),
	})

	err := svrcmd.Execute(rootCmd, "okamid", app.DefaultNodeHome)
	require.NoError(t, err)
}

func TestAddKeyLedgerCmd(t *testing.T) {
	rootCmd, _ := okamid.NewRootCmd()
	rootCmd.SetArgs([]string{
		"keys",
		"add",
		"dev0",
		fmt.Sprintf("--%s", flags.FlagUseLedger),
	})

	err := svrcmd.Execute(rootCmd, "OKAMID", app.DefaultNodeHome)
	require.Error(t, err)
}
