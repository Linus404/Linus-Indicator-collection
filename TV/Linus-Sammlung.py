// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Trader_Linus

//@version=5
indicator("Linus Sammlung", overlay=true, timeframe="", timeframe_gaps=true)

//#region                   Moving Averages
//#region                      Constants
var DEFAULT_LINEWIDTH   = 1
var DEFAULT_COLOR1      = color.new(#c9daf8, 5)
var DEFAULT_COLOR2      = color.new(#a4c2f4, 5)
var DEFAULT_COLOR3      = color.new(#6d9eeb, 5)
var DEFAULT_COLOR4      = color.new(#3c78d8, 5)
var DEFAULT_COLOR5      = color.new(#0b5394, 5)
//#endregion


//#region                        Inputs
// Groups
g1 = "#1"
g2 = "#2"
g3 = "#3"
g4 = "#4"
g5 = "#5"
g6 = "Preferences"


// Tooltips
tt_timeframe    = "You can display a Moving Average from a higher timeframe. " +
                     "Note: It will be automatically hidden when switching the chart to a timeframe higher than its timeframe."


// Inputs
i_type_1        = input.string      ("EMA", "Type", ["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"],    group=g1)
i_length1       = input.int         (9,    "Length", 1,                                             group=g1)
i_source1       = input             (close, "Source",                                               group=g1)
i_offset1       = input.int         (0,     "Offset",                                               group=g1)
i_timeframe1    = input.timeframe   ("",    "Timeframe", tooltip=tt_timeframe,                      group=g1)

i_type_2        = input.string      ("EMA", "Type", ["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"],    group=g2)
i_length2       = input.int         (20,    "Length", 1,                                            group=g2)
i_source2       = input             (close, "Source",                                               group=g2)
i_offset2       = input.int         (0,     "Offset",                                               group=g2)
i_timeframe2    = input.timeframe   ("",    "Timeframe", tooltip=tt_timeframe,                      group=g2)

i_type_3        = input.string      ("EMA", "Type", ["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"],    group=g3)
i_length3       = input.int         (50,    "Length", 1,                                            group=g3)
i_source3       = input             (close, "Source",                                               group=g3)
i_offset3       = input.int         (0,     "Offset",                                               group=g3)
i_timeframe3    = input.timeframe   ("",    "Timeframe", tooltip=tt_timeframe,                      group=g3)

i_type_4        = input.string      ("EMA", "Type", ["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"],    group=g4)
i_length4       = input.int         (100,   "Length", 1,                                            group=g4)
i_source4       = input             (close, "Source",                                               group=g4)
i_offset4       = input.int         (0,     "Offset",                                               group=g4)
i_timeframe4    = input.timeframe   ("",    "Timeframe", tooltip=tt_timeframe,                      group=g4)

i_type_5        = input.string      ("EMA", "Type", ["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"],    group=g5)
i_length5       = input.int         (200,   "Length", 1,                                            group=g5)
i_source5       = input             (close, "Source",                                               group=g5)
i_offset5       = input.int         (0,     "Offset",                                               group=g5)
i_timeframe5    = input.timeframe   ("",    "Timeframe", tooltip=tt_timeframe,                      group=g5)

i_enableGaps    = input             (true,  "Wait for timeframe closes",                            group=g6)
//#endregion


//#region                       Functions 
// @function Get the Moving Average (MA)
// @returns float
f_getMa(string _type, float _source, _length) =>
    switch _type
        "SMA"           => ta.sma(_source, _length)
        "EMA"           => ta.ema(_source, _length)
        "SMMA (RMA)"    => ta.rma(_source, _length)
        "WMA"           => ta.wma(_source, _length)
        "VWMA"          => ta.vwma(_source, _length)


// @function Check if a timeframe is higher or equal than the chart's one
// @returns bool
f_canDisplay(_tf) =>
    timeframe.in_seconds(_tf) >= timeframe.in_seconds()
//#endregion


//#region                         Logic
var gaps = i_enableGaps ? barmerge.gaps_on : barmerge.gaps_off

ma1 = request.security(syminfo.tickerid, i_timeframe1, f_getMa(i_type_1, i_source1, i_length1), gaps=gaps)
ma2 = request.security(syminfo.tickerid, i_timeframe2, f_getMa(i_type_2, i_source2, i_length2), gaps=gaps)
ma3 = request.security(syminfo.tickerid, i_timeframe3, f_getMa(i_type_3, i_source3, i_length3), gaps=gaps)
ma4 = request.security(syminfo.tickerid, i_timeframe4, f_getMa(i_type_4, i_source4, i_length4), gaps=gaps)
ma5 = request.security(syminfo.tickerid, i_timeframe5, f_getMa(i_type_5, i_source5, i_length5), gaps=gaps)
//#endregion


//#region                   Plotting & styling
plot(f_canDisplay(i_timeframe1) ? ma1 : na, "#1", DEFAULT_COLOR1, DEFAULT_LINEWIDTH, offset=i_offset1)
plot(f_canDisplay(i_timeframe2) ? ma2 : na, "#2", DEFAULT_COLOR2, DEFAULT_LINEWIDTH, offset=i_offset2)
plot(f_canDisplay(i_timeframe3) ? ma3 : na, "#3", DEFAULT_COLOR3, DEFAULT_LINEWIDTH, offset=i_offset3)
plot(f_canDisplay(i_timeframe4) ? ma4 : na, "#4", DEFAULT_COLOR4, DEFAULT_LINEWIDTH, offset=i_offset4)
plot(f_canDisplay(i_timeframe5) ? ma5 : na, "#5", DEFAULT_COLOR5, DEFAULT_LINEWIDTH, offset=i_offset5)
//#endregion
//#endregion


//#region                         VWAP
hideonDWM = input(false, title="Hide VWAP on 1D or Above", group="VWAP Settings", display = display.data_window)
var anchor = input.string(defval = "Session", title="Anchor Period",
 options=["Session", "Week", "Month", "Quarter", "Year", "Decade", "Century", "Earnings", "Dividends", "Splits"], group="VWAP Settings")
src = input(title = "Source", defval = hlc3, group="VWAP Settings", display = display.data_window)
offset = input.int(0, title="Offset", group="VWAP Settings", minval=0, display = display.data_window)

BANDS_GROUP = "Bands Settings"
CALC_MODE_TOOLTIP = "Determines the units used to calculate the distance of the bands. When 'Percentage' is selected, a multiplier of 1 means 1%."
calcModeInput = input.string("Standard Deviation", "Bands Calculation Mode", options = ["Standard Deviation", "Percentage"], group = BANDS_GROUP, tooltip = CALC_MODE_TOOLTIP, display = display.data_window)
showBand_1 = input(true, title = "", group = BANDS_GROUP, inline = "band_1", display = display.data_window)
bandMult_1 = input.float(1.0, title = "Bands Multiplier #1", group = BANDS_GROUP, inline = "band_1", step = 0.5, minval=0, display = display.data_window)
showBand_2 = input(false, title = "", group = BANDS_GROUP, inline = "band_2", display = display.data_window)
bandMult_2 = input.float(2.0, title = "Bands Multiplier #2", group = BANDS_GROUP, inline = "band_2", step = 0.5, minval=0, display = display.data_window)
showBand_3 = input(false, title = "", group = BANDS_GROUP, inline = "band_3", display = display.data_window)
bandMult_3 = input.float(3.0, title = "Bands Multiplier #3", group = BANDS_GROUP, inline = "band_3", step = 0.5, minval=0, display = display.data_window)

if barstate.islast and ta.cum(volume) == 0
    runtime.error("No volume is provided by the data vendor.")

new_earnings = request.earnings(syminfo.tickerid, earnings.actual, barmerge.gaps_on, barmerge.lookahead_on, ignore_invalid_symbol=true)
new_dividends = request.dividends(syminfo.tickerid, dividends.gross, barmerge.gaps_on, barmerge.lookahead_on, ignore_invalid_symbol=true)
new_split = request.splits(syminfo.tickerid, splits.denominator, barmerge.gaps_on, barmerge.lookahead_on, ignore_invalid_symbol=true)

isNewPeriod = switch anchor
	"Earnings"  => not na(new_earnings)
	"Dividends" => not na(new_dividends)
	"Splits"    => not na(new_split)
	"Session"   => timeframe.change("D")
	"Week"      => timeframe.change("W")
	"Month"     => timeframe.change("M")
	"Quarter"   => timeframe.change("3M")
	"Year"      => timeframe.change("12M")
	"Decade"    => timeframe.change("12M") and year % 10 == 0
	"Century"   => timeframe.change("12M") and year % 100 == 0
	=> false

isEsdAnchor = anchor == "Earnings" or anchor == "Dividends" or anchor == "Splits"
if na(src[1]) and not isEsdAnchor
	isNewPeriod := true

float vwapValue = na
float upperBandValue1 = na
float lowerBandValue1 = na
float upperBandValue2 = na
float lowerBandValue2 = na
float upperBandValue3 = na
float lowerBandValue3 = na

if not (hideonDWM and timeframe.isdwm)
    [_vwap, _stdevUpper, _] = ta.vwap(src, isNewPeriod, 1)
	vwapValue := _vwap
    stdevAbs = _stdevUpper - _vwap
	bandBasis = calcModeInput == "Standard Deviation" ? stdevAbs : _vwap * 0.01
	upperBandValue1 := _vwap + bandBasis * bandMult_1
	lowerBandValue1 := _vwap - bandBasis * bandMult_1
	upperBandValue2 := _vwap + bandBasis * bandMult_2
	lowerBandValue2 := _vwap - bandBasis * bandMult_2
	upperBandValue3 := _vwap + bandBasis * bandMult_3
	lowerBandValue3 := _vwap - bandBasis * bandMult_3

plot(vwapValue, title="VWAP", color=#2962FF, offset=offset)

upperBand_1 = plot(upperBandValue1, title="Upper Band #1", color=color.green, offset=offset, display = showBand_1 ? display.all : display.none)
lowerBand_1 = plot(lowerBandValue1, title="Lower Band #1", color=color.green, offset=offset, display = showBand_1 ? display.all : display.none)
fill(upperBand_1, lowerBand_1, title="Bands Fill #1", color= color.new(color.green, 95)    , display = showBand_1 ? display.all : display.none)

upperBand_2 = plot(upperBandValue2, title="Upper Band #2", color=color.olive, offset=offset, display = showBand_2 ? display.all : display.none)
lowerBand_2 = plot(lowerBandValue2, title="Lower Band #2", color=color.olive, offset=offset, display = showBand_2 ? display.all : display.none)
fill(upperBand_2, lowerBand_2, title="Bands Fill #2", color= color.new(color.olive, 95)    , display = showBand_2 ? display.all : display.none)

upperBand_3 = plot(upperBandValue3, title="Upper Band #3", color=color.teal, offset=offset, display = showBand_3 ? display.all : display.none)
lowerBand_3 = plot(lowerBandValue3, title="Lower Band #3", color=color.teal, offset=offset, display = showBand_3 ? display.all : display.none)
fill(upperBand_3, lowerBand_3, title="Bands Fill #3", color= color.new(color.teal, 95)    , display = showBand_3 ? display.all : display.none)
//#endregion


//region                         HLC
OHLC_GROUP = "HLC settings"

// Calculate Previous Day High, Low, Close
prevHigh = request.security(syminfo.tickerid, "D", high[0])
prevLow = request.security(syminfo.tickerid, "D", low[0])
prevClose = request.security(syminfo.tickerid, "D", close[0])

// Plot Previous Day High, Low, Close
plot(prevHigh, "Prev Day High", color=color.red, linewidth=2)
plot(prevLow, "Prev Day Low", color=color.green, linewidth=2)
plot(prevClose, "Prev Day Close", color=color.blue, linewidth=2)
//#endregion


//#region                         ATR
ATR_GROUP = "ATR Settings"
showATR = input.bool(true, "Show ATR", group=ATR_GROUP)
atrPeriod = input.int(14, "ATR Period", minval=1, group=ATR_GROUP)
atrMultiplier = input.float(1.0, "ATR Band Multiplier", step=0.1, group=ATR_GROUP)

atrValue = ta.atr(atrPeriod)
upperATRBand = high + atrValue * atrMultiplier
lowerATRBand = low - atrValue * atrMultiplier

plot(showATR ? upperATRBand : na, "Upper ATR Band", color=color.rgb(255, 82, 82, 50), linewidth=1)
plot(showATR ? lowerATRBand : na, "Lower ATR Band", color=color.rgb(255, 82, 82, 50), linewidth=1)
//#endregion
