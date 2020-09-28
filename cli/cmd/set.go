package cmd

import (
	"cli/logic"
	"encoding/json"
	"fmt"
	"github.com/spf13/cobra"
)

var ring int
var strand int

var setCmd = &cobra.Command{
	Use:   "set",
	Short: "set a strand or group of strands into the given color",
}

var setAllCmd = &cobra.Command{
	Use:   "all",
	Short: "set all strands to the given color",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		return processSet(args[0], nil, nil)
	},
}

var setRingCmd = &cobra.Command{
	Use:   "ring",
	Short: "set all strands within the given ring to the given color",
	RunE: func(cmd *cobra.Command, args []string) error {
		if ring <= -1 || ring > 3 {
			return fmt.Errorf("please provide a valid ring identifier")
		}

		return processSet(args[0], &ring, nil)
	},
}

var setStrandCmd = &cobra.Command{
	Use:   "strand",
	Short: "set the given strands within the given ring to the given color",
	RunE: func(cmd *cobra.Command, args []string) error {
		if ring <= -1 || ring > 3 {
			return fmt.Errorf("please provide a valid ring identifier")
		}

		if strand <= -1 {
			return fmt.Errorf("please provide a valid strand identifier")
		}

		return processSet(args[0], &ring, &strand)
	},
}

func init() {
	setRingCmd.Flags().IntVarP(&ring, "ring", "r", -1, "the ring to change.")
	setRingCmd.MarkFlagRequired("ring")

	setStrandCmd.Flags().IntVarP(&ring, "ring", "r", -1, "the ring to which the strand belongs.")
	setStrandCmd.MarkFlagRequired("ring")
	setStrandCmd.Flags().IntVarP(&strand, "strand", "s", -1, "the strand to change.")
	setStrandCmd.MarkFlagRequired("strand")

	setCmd.AddCommand(setAllCmd, setRingCmd, setStrandCmd)
	rootCmd.AddCommand(setCmd)
}

func processSet(value string, ring *int, strand *int) error {
	evt := logic.PaddoEventCommand{
		Operator: "set",
		Ring:     ring,
		Strand:   strand,
	}

	v, err := logic.HexToRGB(value)
	if err != nil {
		return err
	}

	evt.Value = v

	b, err := json.Marshal(logic.PaddoEvent{Commands: []logic.PaddoEventCommand{evt}})
	if err != nil {
		return err
	}

	return nc.Publish(subject, b)
}
