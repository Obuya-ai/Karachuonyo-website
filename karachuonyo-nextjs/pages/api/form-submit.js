import fetch from 'node-fetch';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  const { name, email, phone, message, target } = req.body;

  // SendGrid email (if configured)
  try {
    if (process.env.SENDGRID_API_KEY) {
      await fetch('https://api.sendgrid.com/v3/mail/send', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${process.env.SENDGRID_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          personalizations: [{ to: [{ email: 'obuyafelixm@gmail.com' }] }],
          from: { email: 'no-reply@karachuonyofirst.or.ke', name: 'Karachuonyo First' },
          subject: `[${target||'Form'}] ${name} — ${email}`,
          content: [{ type: 'text/plain', value: `Name: ${name}\nEmail: ${email}\nPhone: ${phone}\n\n${message}` }],
        }),
      });
    }
  } catch (err) {
    console.error('sendgrid failed', err);
  }

  // Google Sheets webhook
  if (process.env.GSHEET_WEBHOOK_URL) {
    fetch(process.env.GSHEET_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, message, target, createdAt: new Date().toISOString() }),
    }).catch(e => console.error('gsheet webhook failed', e));
  }

  res.status(200).json({ ok: true });
}
