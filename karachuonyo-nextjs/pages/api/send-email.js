// pages/api/send-email.js
import nodemailer from 'nodemailer';

export default async function handler(req, res) {
  if(req.method !== 'POST') return res.status(405).end();
  const { to, subject, text, html } = req.body;
  // Supports SendGrid SMTP, Mailgun SMTP, or any SMTP provider
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT ? parseInt(process.env.SMTP_PORT) : 587,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS
    }
  });

  try {
    const info = await transporter.sendMail({
      from: `"Karachuonyo First" <${process.env.SMTP_FROM || 'no-reply@karachuonyofirst.or.ke'}>`,
      to,
      subject,
      text,
      html
    });
    res.status(200).json({ ok: true, info });
  } catch (err) {
    console.error('email send failed', err);
    res.status(500).json({ error: 'send failed' });
  }
}
