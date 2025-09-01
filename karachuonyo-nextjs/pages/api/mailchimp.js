import fetch from 'node-fetch';
export default async function handler(req, res){
  if(req.method !== 'POST') return res.status(405).end();
  const { email, firstName } = req.body;
  const listId = process.env.MAILCHIMP_LIST_ID;
  const dc = process.env.MAILCHIMP_SERVER_PREFIX;
  if(!listId || !dc) return res.status(500).json({ error: 'Mailchimp not configured' });
  const url = `https://${dc}.api.mailchimp.com/3.0/lists/${listId}/members`;
  const body = {
    email_address: email,
    status: 'subscribed',
    merge_fields: { FNAME: firstName || '' }
  };
  const r = await fetch(url, {
    method:'POST',
    headers: {
      Authorization: `apikey ${process.env.MAILCHIMP_API_KEY}`,
      'Content-Type':'application/json'
    },
    body: JSON.stringify(body)
  });
  const data = await r.json();
  if (r.status >= 400) return res.status(r.status).json(data);
  return res.status(200).json({ ok: true });
}
