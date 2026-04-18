const CACHE_NAME = 'nijumaru-v2';
const ASSETS = [
  '/',
  '/index.html',
  '/premium.html',
  '/daily.html',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png',
  '/how-to-use.html',
  '/teaching-tips.html',
  '/kuku-tips.html',
  '/grade-guide.html',
  '/reduce-mistakes.html',
  '/study-habits.html',
  '/fractions-guide.html',
  '/test-prep.html',
  '/calculation-power.html',
  '/device-guide.html',
  '/percentage-guide.html',
  '/faq.html',
  '/privacy.html',
  'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap'
];

// インストール：静的アセットをキャッシュ
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS).catch(() => {});
    })
  );
  self.skipWaiting();
});

// アクティベート：古いキャッシュを削除
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// フェッチ：Network First（ランキングAPIはキャッシュしない）
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // 外部API・AdSense はキャッシュしない
  if (
    url.hostname.includes('googlesyndication') ||
    url.hostname.includes('supabase') ||
    url.hostname.includes('firestore') ||
    url.pathname.includes('/api/')
  ) {
    return;
  }

  // Network First → フォールバックでキャッシュ
  e.respondWith(
    fetch(e.request)
      .then(res => {
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
