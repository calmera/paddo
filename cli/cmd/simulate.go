package cmd

import (
	"github.com/spf13/cobra"
	"time"
)

var interval string

var simulateCmd = &cobra.Command{
	Use:   "simulate",
	Short: "simulate load on a nats subject",
	RunE: func(cmd *cobra.Command, args []string) error {
		duration, err := time.ParseDuration(interval)
		if err != nil {
			return err
		}

		for now := range time.Tick(duration) {
			err := nc.Publish("garbage", []byte(now.String()))
			if err != nil {
				return err
			}
		}

		return nil
	},
}

func init() {
	simulateCmd.Flags().StringVarP(&interval, "interval", "i", "1s", "the interval with a duration indicator (ms, s, m, h)")

	rootCmd.AddCommand(simulateCmd)
}
