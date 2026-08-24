from web3 import Web3
from eth_account import Account
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime

# ==================== CHAINS ====================
CHAINS = {
    "Ethereum": {"rpc": "https://ethereum.publicnode.com", "chain_id": 1, "symbol": "ETH"},
    "Base": {"rpc": "https://mainnet.base.org", "chain_id": 8453, "symbol": "ETH"},
    "Arbitrum": {"rpc": "https://arb1.arbitrum.io/rpc", "chain_id": 42161, "symbol": "ETH"},
    "Optimism": {"rpc": "https://mainnet.optimism.io", "chain_id": 10, "symbol": "ETH"},
    "Polygon": {"rpc": "https://polygon.drpc.org", "chain_id": 137, "symbol": "POL"},
    "BNB Chain": {"rpc": "https://bsc-dataseed.binance.org", "chain_id": 56, "symbol": "BNB"},
    "Gnosis": {"rpc": "https://rpc.gnosischain.com", "chain_id": 100, "symbol": "xDAI"},
    "Linea": {"rpc": "https://rpc.linea.build", "chain_id": 59144, "symbol": "ETH"},
    "Blast": {"rpc": "https://rpc.blast.io", "chain_id": 81457, "symbol": "ETH"},
    "Mode": {"rpc": "https://mainnet.mode.network", "chain_id": 34443, "symbol": "ETH"},
    "Soneium": {"rpc": "https://rpc.soneium.org", "chain_id": 1868, "symbol": "ETH"},
    "Scroll": {"rpc": "https://rpc.scroll.io", "chain_id": 534352, "symbol": "ETH"},
    "Mantle": {"rpc": "https://rpc.mantle.xyz", "chain_id": 5000, "symbol": "MNT"},
    "zkSync Era": {"rpc": "https://mainnet.era.zksync.io", "chain_id": 324, "symbol": "ETH"},
    "Avalanche": {"rpc": "https://api.avax.network/ext/bc/C/rpc", "chain_id": 43114, "symbol": "AVAX"},
    "Custom": {"rpc": "", "chain_id": 0, "symbol": "ETH"}
}

# ==================== FUNCTIONS ====================
def log(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_box.insert(tk.END, f"[{timestamp}] {msg}\n")
    log_box.see(tk.END)
    root.update()

def clear_log():
    log_box.delete(1.0, tk.END)

def copy_address():
    address = "0xbe70630Fdc627C06FaBDB8943ac70e2fDf1e10B4"
    root.clipboard_clear()
    root.clipboard_append(address)
    root.update()
    messagebox.showinfo("Copied!", "Address copied to clipboard ✅\nThank you! ☕")

def show_success_window(chain_name, tx_hash):
    success = tk.Toplevel()
    success.title("Success")
    success.geometry("520x280")
    success.configure(bg="#0d1117")
    success.resizable(True, True)

    card = tk.Frame(success, bg="#161b22", bd=0, highlightthickness=1, highlightbackground="#30363d")
    card.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(card, text="✅ Success!", font=("Segoe UI", 18, "bold"),
             bg="#161b22", fg="#3fb950").pack(pady=(20, 10))

    tk.Label(card, text=f"Chain: {chain_name}", font=("Segoe UI", 12),
             bg="#161b22", fg="#e6edf3").pack()

    tk.Label(card, text="Transaction Hash:", font=("Segoe UI", 10),
             bg="#161b22", fg="#8b949e").pack(pady=(15, 5))

    hash_text = tk.Text(card, height=2, width=58, font=("Consolas", 9),
                        bg="#0d1117", fg="#58a6ff", relief="flat", wrap=tk.WORD,
                        bd=0, highlightthickness=1, highlightbackground="#30363d")
    hash_text.insert(tk.END, tx_hash)
    hash_text.pack(pady=5, padx=15)

    tk.Button(card, text="Close", command=success.destroy,
              bg="#238636", fg="white", font=("Segoe UI", 10, "bold"),
              width=16, relief="flat", cursor="hand2",
              activebackground="#2ea043", bd=0).pack(pady=18)

def suggest_low_gas():
    try:
        chain_name = chain_var.get()
        if chain_name == "Custom":
            rpc = custom_rpc.get().strip()
            if not rpc:
                messagebox.showwarning("Warning", "Please enter a Custom RPC first")
                return
            chain = {"rpc": rpc}
        else:
            chain = CHAINS[chain_name]

        w3 = Web3(Web3.HTTPProvider(chain["rpc"], request_kwargs={'timeout': 15}))
        if not w3.is_connected():
            messagebox.showerror("Error", "Failed to connect to RPC")
            return

        current_gas = w3.eth.gas_price
        current_gwei = float(w3.from_wei(current_gas, "gwei"))

        suggested_priority = max(0.05, round(current_gwei * 0.3, 3))
        suggested_max_fee  = max(suggested_priority * 2, round(current_gwei * 0.8, 3))
        suggested_gas_limit = 80000

        gas_limit_entry.delete(0, tk.END)
        gas_limit_entry.insert(0, str(suggested_gas_limit))

        priority_entry.delete(0, tk.END)
        priority_entry.insert(0, str(suggested_priority))

        maxfee_entry.delete(0, tk.END)
        maxfee_entry.insert(0, str(suggested_max_fee))

        msg = (
            f"Current Network Gas: {current_gwei:.3f} gwei\n\n"
            f"Suggested Low Gas:\n"
            f"• Gas Limit     : {suggested_gas_limit}\n"
            f"• Priority Fee  : {suggested_priority} gwei\n"
            f"• Max Fee       : {suggested_max_fee} gwei\n\n"
            f"Values have been auto-filled."
        )
        messagebox.showinfo("Low Gas Suggestion", msg)
        log(f"Suggested → GasLimit: {suggested_gas_limit} | Priority: {suggested_priority} gwei | MaxFee: {suggested_max_fee} gwei")

    except Exception as e:
        messagebox.showerror("Error", f"Could not suggest gas:\n{str(e)}")

def revoke_delegation():
    clear_log()
    victim_key = victim_entry.get().strip()
    sponsor_key = sponsor_entry.get().strip()
    chain_name = chain_var.get()

    log("Starting revoke process...")

    if not victim_key or not sponsor_key:
        log("ERROR: Both private keys are required!")
        messagebox.showerror("Error", "Please enter both private keys!")
        return

    if not victim_key.startswith("0x"):
        victim_key = "0x" + victim_key
    if not sponsor_key.startswith("0x"):
        sponsor_key = "0x" + sponsor_key

    try:
        try:
            gas_limit = int(gas_limit_entry.get().strip())
            priority_gwei = float(priority_entry.get().strip())
            maxfee_gwei = float(maxfee_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for gas values")
            return

        if gas_limit < 21000:
            messagebox.showerror("Error", "Gas Limit must be at least 21000")
            return

        if chain_name == "Custom":
            rpc = custom_rpc.get().strip()
            chain_id = int(custom_chainid.get().strip())
            if not rpc or not chain_id:
                log("ERROR: Custom RPC and Chain ID are required")
                messagebox.showerror("Error", "Please enter Custom RPC and Chain ID")
                return
            chain = {"rpc": rpc, "chain_id": chain_id, "symbol": "ETH"}
        else:
            chain = CHAINS[chain_name]

        log(f"Selected Chain: {chain_name} (ID: {chain['chain_id']})")
        log(f"Connecting to RPC: {chain['rpc']}")

        w3 = Web3(Web3.HTTPProvider(chain["rpc"], request_kwargs={'timeout': 30}))

        if not w3.is_connected():
            log("ERROR: Failed to connect to RPC")
            messagebox.showerror("Error", f"Could not connect to {chain_name}")
            return

        log("RPC connected successfully")

        victim = Account.from_key(victim_key)
        sponsor = Account.from_key(sponsor_key)

        log(f"Victim Address : {victim.address}")
        log(f"Sponsor Address: {sponsor.address}")

        balance = w3.eth.get_balance(sponsor.address)
        bal_eth = w3.from_wei(balance, "ether")
        log(f"Sponsor Balance: {bal_eth} {chain.get('symbol', '')}")

        if balance < w3.to_wei(0.0001, "ether"):
            log("ERROR: Sponsor balance is too low")
            messagebox.showerror("Error", f"Sponsor balance is too low!\nCurrent: {bal_eth}")
            return

        log("Getting victim nonce...")
        nonce = w3.eth.get_transaction_count(victim.address)
        log(f"Victim Nonce: {nonce}")

        log("Signing EIP-7702 authorization (to zero address)...")
        authorization = {
            "chainId": chain["chain_id"],
            "address": "0x0000000000000000000000000000000000000000",
            "nonce": nonce
        }
        signed_auth = Account.sign_authorization(authorization, private_key=victim_key)
        log("Authorization signed successfully")

        priority_fee = w3.to_wei(priority_gwei, "gwei")
        max_fee = w3.to_wei(maxfee_gwei, "gwei")

        log(f"Using Gas Limit     : {gas_limit}")
        log(f"Priority Fee        : {priority_gwei} gwei")
        log(f"Max Fee Per Gas     : {maxfee_gwei} gwei")

        tx = {
            "type": 4,
            "chainId": chain["chain_id"],
            "nonce": w3.eth.get_transaction_count(sponsor.address),
            "maxFeePerGas": int(max_fee),
            "maxPriorityFeePerGas": int(priority_fee),
            "gas": gas_limit,
            "to": victim.address,
            "value": 0,
            "data": b"",
            "authorizationList": [signed_auth],
        }

        log("Signing transaction with sponsor key...")
        signed_tx = sponsor.sign_transaction(tx)

        log("Sending transaction to network...")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = tx_hash.hex()

        log("=" * 50)
        log(f"SUCCESS! Transaction sent")
        log(f"Tx Hash: {tx_hash_hex}")
        log("=" * 50)

        show_success_window(chain_name, tx_hash_hex)

    except Exception as e:
        error_msg = str(e)
        log("=" * 50)
        log("ERROR OCCURRED:")
        log(error_msg)
        log("=" * 50)
        messagebox.showerror("Error", f"An error occurred:\n\n{error_msg}")

# ==================== SIDEBAR TOGGLE ====================
sidebar_visible = False

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar.pack_forget()
        sidebar_visible = False
        guide_btn.config(text="📖 Guide")
    else:
        sidebar.pack(side="right", fill="y", padx=(0, 0))
        sidebar_visible = True
        guide_btn.config(text="❌ Close")

# ==================== GUI ====================
root = tk.Tk()
root.title("EIP-7702 Revoker | by Coinlover21")
root.geometry("1050x960")
root.minsize(900, 750)          # Minimum size so layout doesn't break
root.resizable(True, True)      # ← Now you can resize, maximize & minimize
root.configure(bg="#0d1117")

# ========== HEADER ==========
header = tk.Frame(root, bg="#0d1117")
header.pack(fill="x", pady=(12, 5))

title_frame = tk.Frame(header, bg="#0d1117")
title_frame.pack(fill="x")

tk.Label(title_frame, text="⚡ EIP-7702 Multi-Chain Revoker", 
         font=("Segoe UI", 18, "bold"), bg="#0d1117", fg="#58a6ff").pack(side="left", padx=(22, 0))

guide_btn = tk.Button(title_frame, text="📖 Guide", command=toggle_sidebar,
                      bg="#238636", fg="white", font=("Segoe UI", 9, "bold"),
                      relief="flat", cursor="hand2", padx=12, pady=4,
                      activebackground="#2ea043", bd=0)
guide_btn.pack(side="right", padx=22)

tk.Label(header, text="Advanced Low Gas Edition", 
         font=("Segoe UI", 10), bg="#0d1117", fg="#8b949e").pack(anchor="w", padx=22)

tk.Label(header, text="Developed by Coinlover21", 
         font=("Segoe UI", 9, "italic"), bg="#0d1117", fg="#7d8590").pack(anchor="w", padx=22, pady=(2, 4))

# ===== Donation Address =====
donation_frame = tk.Frame(header, bg="#161b22", highlightthickness=1, highlightbackground="#30363d")
donation_frame.pack(pady=(6, 8), padx=22, fill="x")

inner_don = tk.Frame(donation_frame, bg="#161b22")
inner_don.pack(pady=8)

tk.Label(inner_don, text="☕ Buy me a Coffee:", 
         font=("Segoe UI", 9), bg="#161b22", fg="#58a6ff").pack(side="left")

tk.Label(inner_don, 
         text="0xbe70630Fdc627C06FaBDB8943ac70e2fDf1e10B4",
         font=("Consolas", 10, "bold"), 
         bg="#161b22", fg="#79c0ff").pack(side="left", padx=8)

tk.Button(inner_don, text="📋 Copy", command=copy_address,
          bg="#238636", fg="white", font=("Segoe UI", 8, "bold"),
          relief="flat", cursor="hand2", padx=10, pady=2,
          activebackground="#2ea043", bd=0).pack(side="left")

# ========== MAIN + SIDEBAR CONTAINER ==========
content = tk.Frame(root, bg="#0d1117")
content.pack(fill="both", expand=True, padx=0)

# ========== MAIN CONTENT ==========
main = tk.Frame(content, bg="#0d1117")
main.pack(side="left", fill="both", expand=True, padx=22)

# Keys Section
tk.Label(main, text="Victim Private Key (Compromised)", 
         font=("Segoe UI", 9, "bold"), bg="#0d1117", fg="#e6edf3").pack(anchor="w", pady=(4, 0))
victim_entry = tk.Entry(main, width=90, show="*", font=("Consolas", 10),
                        bg="#161b22", fg="#e6edf3", insertbackground="#58a6ff",
                        relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
victim_entry.pack(pady=(3, 2), ipady=6, fill="x")

# Privacy note under Victim key
tk.Label(main, text="🔒 Your private keys never leave your device. They are processed only locally on your system.",
         font=("Segoe UI", 8), bg="#0d1117", fg="#8b949e").pack(anchor="w", pady=(0, 8))

tk.Label(main, text="Sponsor Private Key (Gas Sponsor)", 
         font=("Segoe UI", 9, "bold"), bg="#0d1117", fg="#e6edf3").pack(anchor="w")
sponsor_entry = tk.Entry(main, width=90, show="*", font=("Consolas", 10),
                         bg="#161b22", fg="#e6edf3", insertbackground="#58a6ff",
                         relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
sponsor_entry.pack(pady=(3, 2), ipady=6, fill="x")

# Privacy note under Sponsor key
tk.Label(main, text="🔒 Your private keys never leave your device. They are processed only locally on your system.",
         font=("Segoe UI", 8), bg="#0d1117", fg="#8b949e").pack(anchor="w", pady=(0, 10))

# Chain
chain_frame = tk.Frame(main, bg="#0d1117")
chain_frame.pack(fill="x", pady=4)

tk.Label(chain_frame, text="Select Chain:", font=("Segoe UI", 9, "bold"),
         bg="#0d1117", fg="#e6edf3").pack(side="left")

chain_var = tk.StringVar(value="Base")
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", 
                fieldbackground="#161b22", 
                background="#161b22",
                foreground="#e6edf3", 
                arrowcolor="#58a6ff",
                bordercolor="#30363d",
                lightcolor="#161b22",
                darkcolor="#161b22")
style.map("TCombobox", fieldbackground=[("readonly", "#161b22")])

chain_menu = ttk.Combobox(chain_frame, textvariable=chain_var, 
                          values=list(CHAINS.keys()), state="readonly", width=30,
                          font=("Segoe UI", 9))
chain_menu.pack(side="left", padx=10)

# Custom RPC
custom_frame = tk.Frame(main, bg="#0d1117")
custom_frame.pack(fill="x", pady=6)

tk.Label(custom_frame, text="Custom RPC:", font=("Segoe UI", 9, "bold"),
         bg="#0d1117", fg="#e6edf3").grid(row=0, column=0, sticky="w")
custom_rpc = tk.Entry(custom_frame, width=55, font=("Consolas", 9),
                      bg="#161b22", fg="#58a6ff", insertbackground="#58a6ff",
                      relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
custom_rpc.grid(row=0, column=1, padx=8, ipady=4, sticky="ew")
custom_frame.columnconfigure(1, weight=1)

tk.Label(custom_frame, text="Chain ID:", font=("Segoe UI", 9, "bold"),
         bg="#0d1117", fg="#e6edf3").grid(row=1, column=0, sticky="w", pady=5)
custom_chainid = tk.Entry(custom_frame, width=12, font=("Consolas", 9),
                          bg="#161b22", fg="#58a6ff", insertbackground="#58a6ff",
                          relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
custom_chainid.grid(row=1, column=1, sticky="w", padx=8, ipady=4)

# Gas Settings
gas_frame = tk.LabelFrame(main, text="  ⛽ Gas Settings (Manual / Low Gas)  ",
                          font=("Segoe UI", 9, "bold"), bg="#161b22", fg="#58a6ff",
                          padx=12, pady=10, bd=0, highlightthickness=1, highlightbackground="#30363d")
gas_frame.pack(fill="x", pady=10)

tk.Label(gas_frame, text="Gas Limit:", bg="#161b22", fg="#e6edf3", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
gas_limit_entry = tk.Entry(gas_frame, width=10, font=("Consolas", 9),
                           bg="#0d1117", fg="#e6edf3", insertbackground="#58a6ff",
                           relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
gas_limit_entry.insert(0, "100000")
gas_limit_entry.grid(row=0, column=1, padx=6, ipady=3)

tk.Label(gas_frame, text="Priority Fee (gwei):", bg="#161b22", fg="#e6edf3", font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", padx=(15,0))
priority_entry = tk.Entry(gas_frame, width=8, font=("Consolas", 9),
                          bg="#0d1117", fg="#e6edf3", insertbackground="#58a6ff",
                          relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
priority_entry.insert(0, "1")
priority_entry.grid(row=0, column=3, padx=6, ipady=3)

tk.Label(gas_frame, text="Max Fee (gwei):", bg="#161b22", fg="#e6edf3", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=8)
maxfee_entry = tk.Entry(gas_frame, width=10, font=("Consolas", 9),
                        bg="#0d1117", fg="#e6edf3", insertbackground="#58a6ff",
                        relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
maxfee_entry.insert(0, "2")
maxfee_entry.grid(row=1, column=1, padx=6, ipady=3)

tk.Button(gas_frame, text="⚡ Suggest Low Gas", command=suggest_low_gas,
          bg="#238636", fg="white", font=("Segoe UI", 9, "bold"),
          relief="flat", cursor="hand2", padx=10, pady=3,
          activebackground="#2ea043", bd=0).grid(row=1, column=2, columnspan=2, padx=8)

# Revoke Button
btn_frame = tk.Frame(main, bg="#0d1117")
btn_frame.pack(pady=12)

tk.Button(btn_frame, text="🚀  REVOKE NOW", command=revoke_delegation,
          bg="#238636", fg="white", font=("Segoe UI", 13, "bold"),
          width=20, height=1, relief="flat", cursor="hand2",
          activebackground="#2ea043", bd=0, pady=4).pack()

# Log
tk.Label(main, text="Live Log", font=("Segoe UI", 9, "bold"), bg="#0d1117", fg="#e6edf3").pack(anchor="w", pady=(5, 0))
log_box = scrolledtext.ScrolledText(main, width=88, height=9, font=("Consolas", 9),
                                    bg="#0d1117", fg="#3fb950", insertbackground="#58a6ff",
                                    relief="flat", bd=0, highlightthickness=1, highlightbackground="#30363d")
log_box.pack(pady=4, fill="both", expand=True)

tk.Button(main, text="Clear Log", command=clear_log, width=12,
          bg="#21262d", fg="#e6edf3", relief="flat", cursor="hand2",
          activebackground="#30363d", bd=0, font=("Segoe UI", 9)).pack(pady=6)

# ========== SIDEBAR (Guide) ==========
sidebar = tk.Frame(content, bg="#161b22", width=320, highlightthickness=1, highlightbackground="#30363d")

sidebar_title = tk.Label(sidebar, text="📖 User Guide", font=("Segoe UI", 14, "bold"),
                         bg="#161b22", fg="#58a6ff")
sidebar_title.pack(pady=(15, 10), padx=15, anchor="w")

guide_text = scrolledtext.ScrolledText(sidebar, width=36, height=42, font=("Segoe UI", 9),
                                       bg="#0d1117", fg="#e6edf3", relief="flat",
                                       wrap=tk.WORD, bd=0, highlightthickness=0)
guide_text.pack(padx=12, pady=(0, 15), fill="both", expand=True)

guide_content = """WHAT IS THIS TOOL?

This is an EIP-7702 Multi-Chain Revoker.
It allows you to revoke (cancel) an EIP-7702 authorization / delegation from a compromised wallet.

────────────────────────────────────
WHY DO YOU NEED TO REVOKE?

EIP-7702 lets a wallet temporarily act like a smart contract by delegating its authority to another address.

If your private key was exposed or you previously authorized a malicious contract, that contract may still control your wallet until you revoke the authorization.

Revoking sets the authorization to the zero address, removing the delegation.

────────────────────────────────────
WHAT HAPPENS WHEN YOU REVOKE?

• The tool signs an EIP-7702 authorization pointing to the zero address (0x000...000).
• A Type-4 transaction is sent using the Sponsor wallet to pay gas.
• After confirmation, the previous delegation is cleared.
• Your wallet returns to normal EOA behavior.

────────────────────────────────────
HOW TO USE

1. Enter the Victim Private Key
   (the compromised wallet you want to fix)

2. Enter the Sponsor Private Key
   (a separate wallet that will pay the gas fees)

3. Select the blockchain network
   (or use Custom RPC + Chain ID)

4. Adjust Gas settings if needed
   (or click "Suggest Low Gas")

5. Click "REVOKE NOW"

6. Wait for the transaction to be sent
   and confirm it on a block explorer.

────────────────────────────────────
IMPORTANT NOTES

• 🔒 Your private keys NEVER leave your device.
  They are processed only locally on your system
  and are never sent to any server.

• Never share your private keys with anyone.
• Use this tool only on wallets you own.
• Make sure the Sponsor has enough balance for gas.
• Always double-check the network before sending.
• After success, verify the transaction on the explorer.

────────────────────────────────────
SUPPORT

If this tool helped you, consider buying me a coffee ☕
"""

guide_text.insert(tk.END, guide_content)
guide_text.config(state="disabled")

root.mainloop()