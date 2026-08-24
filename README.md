# ⚡ EIP-7702 Multi-Chain Revoker

**Advanced Low Gas Edition**  
Developed by Coinlover21

A simple & powerful tool to **revoke EIP-7702 authorizations/delegations** from compromised wallets across multiple EVM chains.

---

### 🔥 What is this tool?

EIP-7702 allows EOAs to temporarily act like smart contracts by delegating authority.  
If your wallet was compromised or you authorized a malicious contract, this tool lets you **revoke that delegation** by setting it to the zero address (`0x000...000`).

The tool uses a **Sponsor wallet** to pay gas fees, so the compromised wallet doesn't need funds.

---

### ✅ Supported Chains (15 + Custom)

| #  | Chain          | Chain ID | Native Token |
|----|----------------|----------|--------------|
| 1  | Ethereum       | 1        | ETH          |
| 2  | Base           | 8453     | ETH          |
| 3  | Arbitrum       | 42161    | ETH          |
| 4  | Optimism       | 10       | ETH          |
| 5  | Polygon        | 137      | POL          |
| 6  | BNB Chain      | 56       | BNB          |
| 7  | Gnosis         | 100      | xDAI         |
| 8  | Linea          | 59144    | ETH          |
| 9  | Blast          | 81457    | ETH          |
| 10 | Mode           | 34443    | ETH          |
| 11 | Soneium        | 1868     | ETH          |
| 12 | Scroll         | 534352   | ETH          |
| 13 | Mantle         | 5000     | MNT          |
| 14 | zkSync Era     | 324      | ETH          |
| 15 | Avalanche      | 43114    | AVAX         |
| 16 | **Custom**     | Any      | Any          |

---

### ✨ Features

- Multi-chain support (15 networks + Custom RPC)
- Low Gas Suggestion feature
- Clean modern dark GUI
- Live logging
- Private keys **never leave your device** (100% local processing)
- Sponsor wallet pays the gas
- Type-4 (EIP-7702) transaction support

---

### 📥 Download

**Latest Release (Windows .exe):**  
👉 [Download from Releases](https://github.com/YOUR-USERNAME/EIP-7702-Revoker/releases)

---

### 🛠️ How to Use

1. Open the tool
2. Enter **Victim Private Key** (compromised wallet)
3. Enter **Sponsor Private Key** (wallet that will pay gas)
4. Select the chain (or use Custom RPC + Chain ID)
5. Click **"Suggest Low Gas"** (optional) or set gas manually
6. Click **REVOKE NOW**
7. Confirm the transaction on a block explorer

---

### 🔒 Security Notes

- Your private keys are processed **only locally** on your computer.
- Keys are never sent to any server.
- Always double-check the network before confirming.
- Use this tool **only on wallets you own**.

---

### ☕ Support the Developer

If this tool helped you, consider buying me a coffee:

`0xbe70630Fdc627C06FaBDB8943ac70e2fDf1e10B4`

---

### ⚠️ Disclaimer

This tool is provided for educational and recovery purposes only.  
The developer is not responsible for any loss of funds or misuse.
