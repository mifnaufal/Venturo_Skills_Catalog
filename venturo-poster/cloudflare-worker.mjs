/**
 * Venturo Image Generation Worker
 * Cloudflare Workers AI wrapper for catalog image generation.
 * Accepts POST {"prompt": "..."} and returns raw PNG image binary.
 *
 * Required bindings:
 *   AI -> Cloudflare Workers AI (service binding)
 *
 * Environment variables:
 *   API_KEY -> your secret API key for auth
 */

const MODEL = 'google/nano-banana-2-lite';

export default {
  async fetch(request, env) {
    // CORS headers for browser/MCP callers
    const headers = corsHeaders();

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers });
    }

    if (request.method !== 'POST') {
      return new Response(
        JSON.stringify({ error: 'Only POST allowed' }),
        { status: 405, headers: { ...headers, 'Content-Type': 'application/json' } }
      );
    }

    // Authenticate via X-API-Key header or body field
    const apiKey = request.headers.get('X-API-Key') || '';
    const body = await request.json().catch(() => ({}));
    const bodyApiKey = body.api_key || '';

    if (!apiKey || !bodyApiKey) {
      return new Response(
        JSON.stringify({ error: 'Missing API key. Provide via X-API-Key header or body.api_key' }),
        { status: 401, headers: { ...headers, 'Content-Type': 'application/json' } }
      );
    }

    const validKey = String(env.API_KEY || '');
    if (apiKey !== validKey && bodyApiKey !== validKey) {
      return new Response(
        JSON.stringify({ error: 'Invalid API key' }),
        { status: 403, headers: { ...headers, 'Content-Type': 'application/json' } }
      );
    }

    const prompt = body.prompt || '';
    if (!prompt.trim()) {
      return new Response(
        JSON.stringify({ error: 'Prompt is required' }),
        { status: 400, headers: { ...headers, 'Content-Type': 'application/json' } }
      );
    }

    try {
      const aiParams = {
        prompt: prompt,
        aspect_ratio: body.aspect_ratio || '1:1',
        output_format: body.output_format || 'png',
        resolution: body.resolution || '1K',
      };
      if (Array.isArray(body.image_input) && body.image_input.length > 0) {
        aiParams.image_input = body.image_input.slice(0, 3); // max 3 per schema
      }

      const response = await env.AI.run(MODEL, aiParams);

      // Workers AI returns image as { image: "<base64>" } or raw bytes depending on model
      let imageData;
      if (response && response.image) {
        imageData = Buffer.from(response.image, 'base64');
      } else if (response && response.data) {
        imageData = Buffer.from(response.data);
      } else {
        imageData = Buffer.from(JSON.stringify(response));
      }

      const outputFormat = aiParams.output_format || 'png';
      const mime = outputFormat === 'jpg' ? 'image/jpeg' : 'image/png';

      return new Response(imageData, {
        headers: {
          ...headers,
          'Content-Type': mime,
          'Cache-Control': 'no-cache',
        },
      });
    } catch (err) {
      console.error('Image generation failed:', err.message);
      return new Response(
        JSON.stringify({ error: 'Image generation failed', details: err.message }),
        { status: 500, headers: { ...headers, 'Content-Type': 'application/json' } }
      );
    }
  },
};

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
  };
}
