package logic

import "strconv"

func HexToRGB(hex string) ([]int, error) {
	values, err := strconv.ParseUint(hex, 16, 32)

	if err != nil {
		return nil, err
	}

	return []int{
		int(values >> 16),
		int((values >> 8) & 0xFF),
		int(values & 0xFF),
	}, nil
}
