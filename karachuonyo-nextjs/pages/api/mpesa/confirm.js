// Basic handler to accept M-Pesa STK callback
import fs from 'fs';
export default async function handler(req, res) {
  if(req.method !== 'POST') return res.status(405).end();
  const body = req.body;
  // Persist callback to a file for reconciliation (or write to DB)
  try {
    fs.appendFileSync('/tmp/mpesa_callbacks.log', JSON.stringify(body) + '\n');
  } catch (e) { console.error('log failed', e) }
  // Respond with 200 to Safaricom
  res.status(200).json({ ResultCode: 0, ResultDesc: 'Accepted' });
}
