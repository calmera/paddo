package cmd

import (
	"cli/logic"
	"encoding/json"
	"github.com/spf13/cobra"
)

var clearCmd = &cobra.Command{
	Use:   "clear",
	Short: "clear the paddo of any color",
	RunE: func(cmd *cobra.Command, args []string) error {
		return processClear()
	},
}

func init() {
	rootCmd.AddCommand(clearCmd)
}

func processClear() error {
	evt := logic.PaddoEventCommand{
		Operator: "clear",
	}

	b, err := json.Marshal(logic.PaddoEvent{Commands: []logic.PaddoEventCommand{evt}})
	if err != nil {
		return err
	}

	return nc.Publish(subject, b)
}
