package cmd

import (
	"fmt"
	"os"

	"github.com/nats-io/nats.go"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string
var Version string

var natsServer string
var nc *nats.Conn
var subject = "paddo"

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "paddo",
	Short: "The paddo commandline tool",
	PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
		var err error
		if nc, err = nats.Connect(natsServer); err != nil {
			return err
		}

		return nil
	},
	PersistentPostRunE: func(cmd *cobra.Command, args []string) error {
		if nc != nil && !nc.IsClosed() {
			nc.Close()
		}

		return nil
	},
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute(version string) {
	Version = version

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

	rootCmd.PersistentFlags().StringVarP(&natsServer, "nats", "n", "nats://localhost:4222", "the url to the nats server")
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
	if cfgFile != "" {
		// Use config file from the flag.
		viper.SetConfigFile(cfgFile)
	} else {
		viper.SetConfigName(".paddo")
	}

	viper.SetEnvPrefix("PADDO_")
	viper.AutomaticEnv() // read in environment variables that match

	// If a config file is found, read it in.
	if err := viper.ReadInConfig(); err == nil {
		fmt.Println("Using config file:", viper.ConfigFileUsed())
	}
}
