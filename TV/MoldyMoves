// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Trader_Linus

//@version=5
indicator("MoldyMoves", overlay=true)

// Inputs
minConsecutiveCandles = input.int(4, title="Minimum Consecutive Candles", minval=1)
minMovePercentage = input.float(1.0, title="Minimum Move Percentage", minval=0.1, step=0.1)
highlightColor = input.color(color.new(color.blue, 80), title="Highlight Box Color")
wickHighlightColor = input.color(color.new(color.yellow, 80), title="Wick Highlight Color")
wickBoxSize = input.int(24, title="Wick Highlight Box Size", minval=1)
significantWickPercentage = input.float(0.1, title="Significant Wick Percentage", minval=0.1, step=0.1)

// Function to determine candle color
getCandleColor(open, close) =>
    close > open ? 1 : close < open ? -1 : 0

// Get current candle color
currentColor = getCandleColor(open, close)

// Initialize variables
var int consecutiveCount = 0
var int lastColor = 0
var float moveStartPrice = 0.0
var float moveHighPrice = 0.0
var float moveLowPrice = 0.0
var int moveStartIndex = 0

// Function to check for significant wicks
isSignificantWick(open, high, low, close, basePrice) =>
    upperWick = high - math.max(open, close)
    lowerWick = math.min(open, close) - low
    
    upperWickPercentage = upperWick / basePrice * 100
    lowerWickPercentage = lowerWick / basePrice * 100
    
    [upperWickPercentage > significantWickPercentage, lowerWickPercentage > significantWickPercentage, upperWick, lowerWick]

// Check for color change and consecutive candles
if currentColor != 0
    if currentColor == lastColor
        consecutiveCount += 1
        moveHighPrice := math.max(moveHighPrice, high)
        moveLowPrice := math.min(moveLowPrice, low)
    else
        if consecutiveCount >= minConsecutiveCandles
            priceMove = math.abs(close[1] - moveStartPrice) / moveStartPrice * 100
            if priceMove >= minMovePercentage
                box.new(moveStartIndex, moveHighPrice, bar_index - 1, moveLowPrice, bgcolor=highlightColor, border_color=color.new(color.blue, 50))
                
                // Highlight significant wicks within the move
                for i = 1 to bar_index - moveStartIndex
                    [upperSignificant, lowerSignificant, upperWick, lowerWick] = isSignificantWick(open[i], high[i], low[i], close[i], close[i+1])
                    
                    if upperSignificant
                        wickTop = high[i]
                        wickBottom = math.max(open[i], close[i])
                        box.new(bar_index - i, wickTop, bar_index - i + wickBoxSize, wickBottom, bgcolor=wickHighlightColor, border_color=color.new(color.yellow, 50))
                    
                    if lowerSignificant
                        wickTop = math.min(open[i], close[i])
                        wickBottom = low[i]
                        box.new(bar_index - i, wickTop, bar_index - i + wickBoxSize, wickBottom, bgcolor=wickHighlightColor, border_color=color.new(color.yellow, 50))
        
        consecutiveCount := 1
        lastColor := currentColor
        moveStartPrice := open
        moveHighPrice := high
        moveLowPrice := low
        moveStartIndex := bar_index
else
    consecutiveCount := 0
    lastColor := 0
    moveStartPrice := 0.0
    moveHighPrice := 0.0
    moveLowPrice := 0.0
    moveStartIndex := 0
