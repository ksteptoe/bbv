PITCH = 650
X_BUMP_OFFSET = 105
Y_BUMP_OFFSET = -521
X_OFFSET = 2.5 * PITCH
Y_OFFSET = 7 * PITCH
MARKER = "MARKER"
BUMPS = "BUMPS"
BALLS = "BALLS"
GROUP = {
    "RF": "TRX[0-3]_[TR]X.*",
    "IQ": "TRX[0-3]_ANA_[TR]X_[IQ][PN]",
    "RXG0": "RX_GAIN_.*0|EN_RX.*0|EN_TX.*0",
    "RXG1": "RX_GAIN_.*1|EN_RX.*1|EN_TX.*1",
    "DDR": r"GPIO\[[8-9]\]|GPIO\[1[0-5]\]|IQ_DATA.*|IQ_CLK_.*",
    "JTAG": "T[CMD][KSIO]",
    "CSPI": "CFG_.*",
    "SER": "D2D.*",
    "XTAL": "XTAL_[NP]",
    "MISC": "EN_PWR|WAKE_UP|IRQ|RST|TEST_EN",
    "CLK": "CLK_.*",
}
