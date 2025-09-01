# Karachuonyo First — Next.js Campaign Site

This is a ready-to-deploy Next.js project skeleton for a political campaign:
- React + Next.js pages
- Serverless API endpoints for forms, Mailchimp, M-Pesa (Daraja) STK Push
- PayPal donate integration sample
- Simple Google Sheets webhook example

## Quick start
1. Copy `.env.example` to `.env.local` and fill credentials.
2. `npm install`
3. `npm run dev`
4. Deploy to Vercel and add the same environment variables.

## Files of interest
- `pages/index.js` — main site UI
- `pages/api/form-submit.js` — handles forms (SendGrid + Sheets)
- `pages/api/mailchimp.js` — Mailchimp subscribe
- `pages/api/mpesa/stk.js` — initiate STK Push
- `pages/api/mpesa/confirm.js` — handle M-Pesa callbacks
- `components/DonateButtons.js` — PayPal + M-Pesa buttons

⚠️ Do NOT commit `.env.local` with secrets. Use Vercel environment variables for production.


## Added components & endpoints
- `google_apps_script.gs` — Apps Script webhook to append form submissions to Google Sheets.
- `pages/api/paypal/create-order.js` — server-side PayPal order creation.
- `pages/api/paypal/capture-order.js` — server-side PayPal order capture.
- `pages/api/send-email.js` — SMTP email sender using nodemailer (works with SendGrid SMTP).

## How to use PayPal endpoints
1. Set `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`, and `PAYPAL_ENV` in your `.env.local` or Vercel env.
2. From the client, `POST /api/paypal/create-order` with `{ amount: '10.00', currency: 'USD' }`.
3. Redirect the user to PayPal approval or use the client SDK with the returned order `id`.
4. After approval, call `/api/paypal/capture-order` with `{ orderID }` to capture the payment.

## Apps Script deployment
1. Open the script in the Apps Script editor (Extensions → Apps Script).
2. Deploy → New deployment → select 'Web app'.
3. Set access to 'Anyone' (or restrict as preferred) and copy the Web App URL to `GSHEET_WEBHOOK_URL`.

## SMTP notes
- For SendGrid SMTP: use `SMTP_HOST=smtp.sendgrid.net`, `SMTP_USER=apikey`, and `SMTP_PASS` = your SendGrid API key.
- Do NOT commit real credentials to the repo. Use Vercel environment variables for production.
