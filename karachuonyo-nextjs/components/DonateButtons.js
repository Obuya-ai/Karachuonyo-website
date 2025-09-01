import React from 'react';

export default function DonateButtons() {
  const startMpesa = async () => {
    const phone = prompt('Enter your phone number (2547XXXXXXXX)');
    const amount = prompt('Amount (KES)');
    if(!phone || !amount) return;
    const res = await fetch('/api/mpesa/stk', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ phone, amount })
    });
    const data = await res.json();
    alert('STK Push initiated. Check your phone.');
    console.log(data);
  };

  return (
    <div className="space-y-3">
      <div>
        <button onClick={startMpesa} className="btn bg-yellow-400 w-full">Donate with M-Pesa</button>
      </div>
      <div>
        <div id="paypal-button-container">
          <p className="text-sm">PayPal button will render client-side. Use NEXT_PUBLIC_PAYPAL_CLIENT_ID env var.</p>
        </div>
      </div>
    </div>
  );
}
