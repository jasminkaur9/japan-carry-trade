# The Japan Carry Trade Unwind (2024)

## Background

For 17 years, the Bank of Japan (BOJ) maintained zero or negative interest rates. The yen became the world's preferred funding currency — a foundation for global leverage. Estimates suggest between **$250 billion and $4 trillion** in carry trade positions were built on this assumption.

The carry trade mechanism was simple: borrow cheap yen, buy higher-yielding assets (US Treasuries, equities, emerging market currencies), and pocket the interest rate spread. Japanese investors held massive unhedged positions in US assets.

### What Is a Carry Trade?
A carry trade involves borrowing in a low-interest-rate currency and investing in higher-yielding assets. The profit comes from the interest rate differential (the "carry"). The risk is that the funding currency appreciates, wiping out gains.

## Timeline of Key Events

| Date | Event | Impact |
|------|-------|--------|
| **March 19, 2024** | BOJ ends negative rates for the first time in 17 years | Symbolic shift; markets initially calm |
| **July 31, 2024** | BOJ raises rates to 0.25% + announces reduced bond buying | Double-barrelled tightening — surprise to markets |
| **August 2, 2024** | Weak US jobs report released | Added recession fears on top of yen rally |
| **August 5, 2024** | **Black Monday** — global market crash | Topix -12%, VIX >60, massive global contagion |
| **August 9, 2024** | Markets stabilize | S&P 500 recovers the week's losses |

## Key Data Points (August 5, 2024)

- **Topix**: Fell **12%** — worst day since 1987
- **VIX**: Spiked above **60**, reaching COVID-era levels
- **USD/JPY**: Collapsed from **161 to 142** — a 12% yen surge in days
- **Nikkei 225**: Dropped **4,451 points** — largest ever single-day point decline
- **Mexican Peso**: Worst-hit emerging market currency
- Global strategists described summer 2024 as a **pivot point signaling the end of an era**

## The Contagion Mechanism

The BOJ rate hike on July 31 triggered rapid yen appreciation (USD/JPY moving from 161 to 142). This set off **three simultaneous cascades**:

1. **Japanese investor liquidation**: Japanese investors liquidated US equities to meet margin calls
2. **Carry trade unwinding**: Closing of long positions in Mexican peso (MXN), Brazilian real (BRL), and Australian dollar (AUD)
3. **Global risk-off cascade**: VIX spiked to COVID levels, emerging market currencies crashed, selling in US momentum stocks

### The Contagion Chain
```
BOJ Rate Hike → JPY Appreciation → US Equity Liquidation → EM Currency Crash
     ↓                                      ↓
Margin Calls ←──────────────────── Risk-Off Cascade
```

### Markov Perspective
For 17 years, the transition matrix was stable:
- Probability of BOJ rate hike: <1%
- Probability of yen surging 10%+: <1%

On July 31, 2024, the matrix changed. The probability of a BOJ hike jumped to 15%+. Positions sized for the old probabilities suddenly faced margin calls they were never designed to survive.

## Transfer Entropy: Measuring Directional Information Flow

### Definition
Transfer entropy measures the **directional flow of information** between time series. Unlike correlation, it tells you not just that assets move together, but **who leads and who follows**.

### Formula
```
TE(X → Y) = H(Y_future | Y_past) − H(Y_future | Y_past, X_past)
```

In plain language: **How much does knowing X's history reduce my uncertainty about Y's future?** If that reduction is large, information is flowing from X to Y.

### Transfer Entropy vs. Correlation

| Property | Correlation | Transfer Entropy |
|----------|-------------|-----------------|
| **Question** | Do X and Y move together? | Does X lead Y? |
| **Symmetry** | Symmetric: corr(X,Y) = corr(Y,X) | **Asymmetric**: TE(X→Y) ≠ TE(Y→X) |
| **Direction** | No directional information | Reveals direction of information flow |
| **During stress** | Spikes (correlation compression) | Reveals causal chain |

### Key Findings During the Carry Trade Unwind

1. **TE(JPY → SPX) >> TE(SPX → JPY)**: Yen moves predicted S&P movements, not the reverse
2. **TE(SPX → MXN) >> TE(MXN → SPX)**: S&P moves predicted peso movements
3. **Complete causal chain**: **JPY → SPX → MXN**

This quantifies the direction of information flow — not just that things moved together.

### Why Correlation Fails During Stress (Correlation Compression)
- **Normal times (H1 2024)**: Correlation between SPX and MXN ≈ 0.4 (meaningful diversification)
- **Stress event (August 5)**: Correlation spiked to ≈ 0.9 (diversification collapsed)
- High correlation tells you nothing about **causation**
- Transfer entropy reveals **which asset is driving which**, even when correlations spike

## DRIVER Framework Application

| Phase | Application |
|-------|-------------|
| **Discover** | Find high-frequency data for JPY, SPX, and MXN (July–August 2024) |
| **Represent** | Map the hypothesized contagion chain with expected transfer entropy directions |
| **Implement** | Calculate the transfer entropy matrix; test for statistical significance |
| **Validate** | Does TE(JPY→SPX) exceed the reverse? Does the chain hold? |
| **Evolve** | Can this framework detect future carry trade unwinds? |
| **Reflect** | How is directional causation fundamentally different from correlation? |

## Course Context

This is **Case 5** of MGMT 69000: Mastering AI for Finance at Purdue University.

Course arc:
- Week 1: Tariff shock — policy shock and textual entropy
- Week 3: ChatGPT — sample space expansion
- Week 4: GENIUS Act — regulatory entropy
- Week 5: European energy crisis — irreversibility markers
- **Week 6: Japan carry trade — directional information flow via transfer entropy**
- Week 7: China's property crisis — structural collapse + transfer entropy

## Key Insight

> **Correlation tells you that assets move together. Transfer entropy tells you who leads and who follows.** In a world of interconnected markets, understanding the direction of information flow isn't just academic — it's the difference between **reacting to a crisis** and **anticipating one**.

## Supplementary Data (BIS Bulletin No. 90)

The Bank for International Settlements documented the carry trade unwind in their August 2024 bulletin:

- The yen carry trade had grown substantially during 2022–2024 as the interest rate differential between Japan and other major economies widened
- Non-commercial (speculative) short yen positions on the CME reached record levels by mid-2024
- The unwinding was amplified by:
  - Algorithmic trading strategies that triggered simultaneous liquidation
  - Cross-asset margin calls creating feedback loops
  - Low summer liquidity magnifying price impacts
- The BIS noted that carry trade positions are inherently fragile: they generate small, steady returns but face catastrophic losses when funding currencies appreciate sharply (negative skew)
- The episode highlighted systemic risks from concentrated positioning in currency markets
