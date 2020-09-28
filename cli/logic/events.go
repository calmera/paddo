package logic

type PaddoEvent struct {
	Commands []PaddoEventCommand `json:"commands"`
}

type PaddoEventCommand struct {
	Operator string      `json:"op"`
	Ring     *int        `json:"ring,omitempty"`
	Strand   *int        `json:"strand,omitempty"`
	Value    interface{} `json:"value"`
}
