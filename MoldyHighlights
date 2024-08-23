using System;
using System.Collections.Generic;
using NinjaTrader.Cbi;
using NinjaTrader.Gui;
using NinjaTrader.Gui.Chart;
using NinjaTrader.NinjaScript;
using NinjaTrader.Core.FloatingPoint;
using NinjaTrader.NinjaScript.DrawingTools;
using System.Windows.Media;

namespace NinjaTrader.NinjaScript.Indicators
{
    public class MarkImportantLevels : Indicator
    {
        private double onh, onl, priorSettlement, dayHigh, dayLow, weekHigh, weekLow, monthHigh, monthLow, yearHigh, yearLow, allTimeHigh;
        private DateTime monthStart, yearStart;
        private bool isNewDay, isNewWeek, isNewMonth, isNewYear;
        private Dictionary<string, double> levels;

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = @"Marks important levels on the chart such as Overnight High/Low, Prior Settlement, Daily High/Low, etc.";
                Name = "MarkImportantLevels";
                Calculate = Calculate.OnEachTick;
                IsOverlay = true;
            }
            else if (State == State.DataLoaded)
            {
                onh = double.MinValue;
                onl = double.MaxValue;
                priorSettlement = 0;
                dayHigh = double.MinValue;
                dayLow = double.MaxValue;
                weekHigh = double.MinValue;
                weekLow = double.MaxValue;
                monthHigh = double.MinValue;
                monthLow = double.MaxValue;
                yearHigh = double.MinValue;
                yearLow = double.MaxValue;
                allTimeHigh = double.MinValue;
                levels = new Dictionary<string, double>();
            }
        }

        protected override void OnBarUpdate()
        {
            if (CurrentBar == 0)
            {
                monthStart = Time[0];
                yearStart = Time[0];
                return;
            }

            isNewDay = Time[0].Date != Time[1].Date;
            isNewWeek = isNewDay && Time[0].DayOfWeek < Time[1].DayOfWeek;
            isNewMonth = Time[0].Month != Time[1].Month;
            isNewYear = Time[0].Year != Time[1].Year;

            if (Time[0].TimeOfDay < new TimeSpan(15, 30, 0))
            {
                onh = Math.Max(onh, High[0]);
                onl = Math.Min(onl, Low[0]);
            }

            if (Time[0].TimeOfDay == new TimeSpan(16, 0, 0))
            {
                priorSettlement = Close[0];
            }

            if (isNewDay)
            {
                dayHigh = High[0];
                dayLow = Low[0];
            }
            else
            {
                dayHigh = Math.Max(dayHigh, High[0]);
                dayLow = Math.Min(dayLow, Low[0]);
            }

            if (isNewWeek)
            {
                weekHigh = High[0];
                weekLow = Low[0];
            }
            else
            {
                weekHigh = Math.Max(weekHigh, High[0]);
                weekLow = Math.Min(weekLow, Low[0]);
            }

            if (isNewMonth)
            {
                monthHigh = High[0];
                monthLow = Low[0];
                monthStart = Time[0];
            }
            else
            {
                monthHigh = Math.Max(monthHigh, High[0]);
                monthLow = Math.Min(monthLow, Low[0]);
            }

            if (isNewYear)
            {
                yearHigh = High[0];
                yearLow = Low[0];
                yearStart = Time[0];
            }
            else
            {
                yearHigh = Math.Max(yearHigh, High[0]);
                yearLow = Math.Min(yearLow, Low[0]);
            }

            allTimeHigh = Math.Max(allTimeHigh, High[0]);

            if (IsFirstTickOfBar)
            {
                // Update levels dictionary
                levels.Clear();
                levels["ONH"] = onh;
                levels["ONL"] = onl;
                levels["PriorSettlement"] = priorSettlement;
                levels["DayHigh"] = dayHigh;
                levels["DayLow"] = dayLow;
                levels["WeekHigh"] = weekHigh;
                levels["WeekLow"] = weekLow;
                levels["MonthHigh"] = monthHigh;
                levels["MonthLow"] = monthLow;
                levels["YearHigh"] = yearHigh;
                levels["YearLow"] = yearLow;
                levels["ATH"] = allTimeHigh;

                // Drawing lines
                foreach (var level in levels)
                {
                    Draw.Line(this, level.Key, false, 0, level.Value, CurrentBar, level.Value, GetBrushForLevel(level.Key), DashStyleHelper.Solid, 2);
                }

                // Drawing text labels
                DrawSmartText("ONHText", "Overnight High", onh, GetBrushForLevel("ONH"));
                DrawSmartText("ONLText", "Overnight Low", onl, GetBrushForLevel("ONL"));
                DrawSmartText("PriorSettlementText", "Prior Settlement", priorSettlement, GetBrushForLevel("PriorSettlement"));
                DrawSmartText("DayHighText", "Day High", dayHigh, GetBrushForLevel("DayHigh"));
                DrawSmartText("DayLowText", "Day Low", dayLow, GetBrushForLevel("DayLow"));
                DrawSmartText("WeekHighText", "Week High", weekHigh, GetBrushForLevel("WeekHigh"));
                DrawSmartText("WeekLowText", "Week Low", weekLow, GetBrushForLevel("WeekLow"));
                DrawSmartText("MonthHighText", "Month High", monthHigh, GetBrushForLevel("MonthHigh"));
                DrawSmartText("MonthLowText", "Month Low", monthLow, GetBrushForLevel("MonthLow"));
                DrawSmartText("YearHighText", "Year High", yearHigh, GetBrushForLevel("YearHigh"));
                DrawSmartText("YearLowText", "Year Low", yearLow, GetBrushForLevel("YearLow"));
                DrawSmartText("ATHText", "All-Time High", allTimeHigh, GetBrushForLevel("ATH"));
            }
        }

        private Brush GetBrushForLevel(string levelKey)
        {
            switch (levelKey)
            {
                case "ONH":
                case "ONL":
                    return Brushes.Orange;
                case "PriorSettlement":
                    return Brushes.Yellow;
                case "DayHigh":
                case "DayLow":
                    return Brushes.Red;
                case "WeekHigh":
                case "WeekLow":
                    return Brushes.Magenta;
                case "MonthHigh":
                case "MonthLow":
                    return Brushes.Green;
                case "YearHigh":
                case "YearLow":
                    return Brushes.Blue;
                case "ATH":
                    return Brushes.Gold;
                default:
                    return Brushes.White;
            }
        }

        private void DrawSmartText(string tag, string text, double yValue, Brush color)
        {
            const int textOffset = 5;
            const double minSpacing = 15;

            // Find a suitable Y position for the text
            double textY = yValue - (TickSize * textOffset);
            bool positionFound = false;

            while (!positionFound)
            {
                positionFound = true;
                foreach (var level in levels)
                {
                    if (Math.Abs(level.Value - textY) < minSpacing)
                    {
                        textY -= minSpacing;
                        positionFound = false;
                        break;
                    }
                }
            }

            Draw.Text(this, tag, text, 0, textY, color);
        }
    }
}

#region NinjaScript generated code. Neither change nor remove.

namespace NinjaTrader.NinjaScript.Indicators
{
	public partial class Indicator : NinjaTrader.Gui.NinjaScript.IndicatorRenderBase
	{
		private MarkImportantLevels[] cacheMarkImportantLevels;
		public MarkImportantLevels MarkImportantLevels()
		{
			return MarkImportantLevels(Input);
		}

		public MarkImportantLevels MarkImportantLevels(ISeries<double> input)
		{
			if (cacheMarkImportantLevels != null)
				for (int idx = 0; idx < cacheMarkImportantLevels.Length; idx++)
					if (cacheMarkImportantLevels[idx] != null &&  cacheMarkImportantLevels[idx].EqualsInput(input))
						return cacheMarkImportantLevels[idx];
			return CacheIndicator<MarkImportantLevels>(new MarkImportantLevels(), input, ref cacheMarkImportantLevels);
		}
	}
}

namespace NinjaTrader.NinjaScript.MarketAnalyzerColumns
{
	public partial class MarketAnalyzerColumn : MarketAnalyzerColumnBase
	{
		public Indicators.MarkImportantLevels MarkImportantLevels()
		{
			return indicator.MarkImportantLevels(Input);
		}

		public Indicators.MarkImportantLevels MarkImportantLevels(ISeries<double> input )
		{
			return indicator.MarkImportantLevels(input);
		}
	}
}

namespace NinjaTrader.NinjaScript.Strategies
{
	public partial class Strategy : NinjaTrader.Gui.NinjaScript.StrategyRenderBase
	{
		public Indicators.MarkImportantLevels MarkImportantLevels()
		{
			return indicator.MarkImportantLevels(Input);
		}

		public Indicators.MarkImportantLevels MarkImportantLevels(ISeries<double> input )
		{
			return indicator.MarkImportantLevels(input);
		}
	}
}

#endregion
