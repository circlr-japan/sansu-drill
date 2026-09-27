/* にじゅうまる。家庭学習の記録コンポーネント（依存なし）
 *
 *   <div data-record-kit="kuku"></div>        九九記録表（問題・正誤・回答時間・日付＋9×9ヒートマップ）
 *   <div data-record-kit="division"></div>    わり算ミス分類（九九・商・ひき算・おろし忘れ・0の扱い）
 *   <div data-record-kit="bunshoudai"></div>  文章題ミス分類（演算選択・数字読み違い・単位・読み飛ばし）
 *   <script src="/record-kit.js" defer></script>
 *
 * 記録はこのブラウザの localStorage にだけ保存する（サーバーには送らない）。
 * 「記録をJSONでコピー」で書き出したものを、実践研究室の記事の実データとして使う。
 */
(function () {
  'use strict';

  var CATS = {
    division: { title: 'わり算のミス分類', items: ['九九', '商のたて方', 'ひき算', 'おろし忘れ', '0の扱い'] },
    bunshoudai: { title: '文章題のミス分類', items: ['演算の選びまちがい', '数字の読みちがい', '単位', '問題文の読み飛ばし'] }
  };

  function load(key) {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) { return []; }
  }
  function save(key, rows) {
    try { localStorage.setItem(key, JSON.stringify(rows)); } catch (e) { /* 保存できない環境では表示のみ */ }
  }
  function today() {
    var d = new Date();
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function copyJSON(type, rows, btn) {
    var text = JSON.stringify({ kit: type, exported: today(), rows: rows }, null, 1);
    var done = function () { btn.textContent = 'コピーしました'; setTimeout(function () { btn.textContent = '記録をJSONでコピー'; }, 1600); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { window.prompt('コピーしてください', text); });
    } else {
      window.prompt('コピーしてください', text);
    }
  }

  /* ── 九九記録表 ── */
  function kuku(root, key) {
    var rows = load(key);
    root.innerHTML = '';
    root.appendChild(el('div', { 'class': 'rk-title' }, '九九の記録表'));
    var form = el('form', { 'class': 'rk-form' },
      '<label>問題 <input name="q" placeholder="7×8" required pattern="[1-9][×xX*][1-9]" inputmode="text" size="5"></label>' +
      '<label>正誤 <select name="ok"><option value="1">○</option><option value="0">×</option></select></label>' +
      '<label>時間 <input name="sec" type="number" min="0" step="0.1" placeholder="秒" size="4"></label>' +
      '<label>日付 <input name="date" type="date"></label>' +
      '<button type="submit">追加</button>');
    form.date.value = today();
    root.appendChild(form);
    var heat = el('div', { 'class': 'rk-heat' });
    var list = el('div', { 'class': 'rk-list' });
    root.appendChild(heat);
    root.appendChild(list);
    var tools = el('div', { 'class': 'rk-tools' });
    var copy = el('button', { type: 'button' }, '記録をJSONでコピー');
    tools.appendChild(copy);
    root.appendChild(tools);

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var m = form.q.value.match(/^([1-9])[×xX*]([1-9])$/);
      if (!m) return;
      rows.push({ a: +m[1], b: +m[2], ok: form.ok.value === '1', sec: form.sec.value === '' ? null : +form.sec.value, date: form.date.value || today() });
      save(key, rows);
      form.q.value = ''; form.sec.value = '';
      draw();
    });
    copy.addEventListener('click', function () { copyJSON('kuku', rows, copy); });

    function draw() {
      // 9×9ヒートマップ：×の割合で色を濃く、セルに回数を表示
      var n = {}, miss = {}, t = {};
      rows.forEach(function (r) {
        var k = r.a + 'x' + r.b;
        n[k] = (n[k] || 0) + 1;
        if (!r.ok) miss[k] = (miss[k] || 0) + 1;
        if (r.sec != null) t[k] = (t[k] || []).concat(r.sec);
      });
      var c = 26, svg = '<svg viewBox="0 0 ' + (c * 10 + 4) + ' ' + (c * 10 + 4) + '" role="img" aria-label="九九の記録のヒートマップ。×が多いマスほど赤が濃い">';
      for (var i = 1; i <= 9; i++) {
        svg += '<text x="' + (c * i + c / 2) + '" y="' + (c * 0.7) + '" font-size="11" text-anchor="middle" fill="#1E3A8A">' + i + '</text>';
        svg += '<text x="' + (c / 2) + '" y="' + (c * i + c * 0.65) + '" font-size="11" text-anchor="middle" fill="#1E3A8A">' + i + '</text>';
        for (var j = 1; j <= 9; j++) {
          var k = i + 'x' + j, tot = n[k] || 0, rate = tot ? (miss[k] || 0) / tot : 0;
          var fill = tot ? 'rgba(220,38,38,' + (0.12 + rate * 0.78).toFixed(2) + ')' : '#F8FAFC';
          var avg = t[k] ? (t[k].reduce(function (s, v) { return s + v; }, 0) / t[k].length).toFixed(1) + '秒' : '';
          svg += '<rect x="' + (c * j) + '" y="' + (c * i) + '" width="' + (c - 2) + '" height="' + (c - 2) + '" rx="3" fill="' + fill + '"><title>' + i + '×' + j + ' 記録' + tot + '回 ×' + (miss[k] || 0) + '回 ' + avg + '</title></rect>';
          if (tot) svg += '<text x="' + (c * j + c / 2 - 1) + '" y="' + (c * i + c * 0.62) + '" font-size="10" text-anchor="middle" fill="#fff">' + (miss[k] || 0) + '/' + tot + '</text>';
        }
      }
      heat.innerHTML = svg + '</svg><p class="rk-note">マスの数字は「×の回数／記録の回数」。赤が濃いマスが、練習に回す九九です。</p>';
      list.innerHTML = rows.length
        ? '<table><tr><th>日付</th><th>問題</th><th>正誤</th><th>時間</th><th></th></tr>' + rows.map(function (r, idx) {
            return '<tr><td>' + esc(r.date) + '</td><td>' + r.a + '×' + r.b + '</td><td>' + (r.ok ? '○' : '×') + '</td><td>' + (r.sec == null ? '' : r.sec + '秒') +
              '</td><td><button type="button" data-del="' + idx + '" aria-label="この行を消す">✕</button></td></tr>';
          }).reverse().join('') + '</table>'
        : '<p class="rk-note">まだ記録がありません。上の欄から追加してください。</p>';
      list.querySelectorAll('[data-del]').forEach(function (b) {
        b.addEventListener('click', function () { rows.splice(+b.getAttribute('data-del'), 1); save(key, rows); draw(); });
      });
    }
    draw();
  }

  /* ── ミス分類（わり算・文章題） ── */
  function tally(root, key, type) {
    var def = CATS[type], rows = load(key);
    root.innerHTML = '';
    root.appendChild(el('div', { 'class': 'rk-title' }, def.title));
    var date = el('input', { type: 'date', 'aria-label': '日付' });
    date.value = today();
    var bar = el('div', { 'class': 'rk-form' });
    bar.appendChild(el('label', {}, '日付 ')).appendChild(date);
    def.items.forEach(function (name) {
      var b = el('button', { type: 'button' }, '＋ ' + esc(name));
      b.addEventListener('click', function () { rows.push({ cat: name, date: date.value || today() }); save(key, rows); draw(); });
      bar.appendChild(b);
    });
    root.appendChild(bar);
    var chart = el('div', { 'class': 'rk-heat' });
    var list = el('div', { 'class': 'rk-list' });
    root.appendChild(chart);
    root.appendChild(list);
    var tools = el('div', { 'class': 'rk-tools' });
    var undo = el('button', { type: 'button' }, '最後の1件を取り消す');
    var copy = el('button', { type: 'button' }, '記録をJSONでコピー');
    tools.appendChild(undo); tools.appendChild(copy);
    root.appendChild(tools);
    undo.addEventListener('click', function () { rows.pop(); save(key, rows); draw(); });
    copy.addEventListener('click', function () { copyJSON(type, rows, copy); });

    function draw() {
      var tot = {}, max = 1;
      def.items.forEach(function (n) { tot[n] = 0; });
      rows.forEach(function (r) { if (r.cat in tot) { tot[r.cat]++; max = Math.max(max, tot[r.cat]); } });
      var h = 26, w = 300, svg = '<svg viewBox="0 0 460 ' + (def.items.length * h + 8) + '" role="img" aria-label="' + def.title + 'の件数のグラフ">';
      def.items.forEach(function (n, i) {
        var len = Math.round(w * tot[n] / max);
        svg += '<text x="146" y="' + (i * h + 18) + '" font-size="12" text-anchor="end" fill="#374151">' + esc(n) + '</text>' +
          '<rect x="152" y="' + (i * h + 6) + '" width="' + Math.max(len, 1) + '" height="16" rx="3" fill="#F59E0B"/>' +
          '<text x="' + (158 + len) + '" y="' + (i * h + 18) + '" font-size="12" fill="#92400E">' + tot[n] + '</text>';
      });
      chart.innerHTML = svg + '</svg>';
      var byDate = {};
      rows.forEach(function (r) { (byDate[r.date] = byDate[r.date] || {})[r.cat] = ((byDate[r.date] || {})[r.cat] || 0) + 1; });
      var dates = Object.keys(byDate).sort().reverse();
      list.innerHTML = dates.length
        ? '<table><tr><th>日付</th>' + def.items.map(function (n) { return '<th>' + esc(n) + '</th>'; }).join('') + '</tr>' +
          dates.map(function (d) { return '<tr><td>' + esc(d) + '</td>' + def.items.map(function (n) { return '<td>' + (byDate[d][n] || '') + '</td>'; }).join('') + '</tr>'; }).join('') + '</table>'
        : '<p class="rk-note">まだ記録がありません。まちがいの種類のボタンを押して記録します。</p>';
    }
    draw();
  }

  function init() {
    if (!document.getElementById('rk-style')) {
      var st = el('style', { id: 'rk-style' },
        '[data-record-kit]{background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:14px 16px;margin:16px 0;font-size:13px;color:#1E293B;}' +
        '.rk-title{font-weight:700;color:#122A64;margin-bottom:8px;}' +
        '.rk-form{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px;}' +
        '.rk-form input,.rk-form select{font:inherit;padding:4px 6px;border:1px solid #CBD5E1;border-radius:6px;}' +
        '[data-record-kit] button{font:inherit;font-size:12px;padding:5px 10px;border:1px solid #CBD5E1;border-radius:999px;background:#F8FAFC;cursor:pointer;}' +
        '.rk-heat svg{width:100%;max-width:460px;height:auto;display:block;}' +
        '.rk-list{overflow-x:auto;}.rk-list table{border-collapse:collapse;font-size:12px;margin-top:8px;}' +
        '.rk-list th,.rk-list td{border:1px solid #E2E8F0;padding:4px 8px;text-align:center;}' +
        '.rk-note{font-size:12px;color:#64748B;margin:6px 0;}.rk-tools{display:flex;gap:8px;margin-top:10px;}');
      document.head.appendChild(st);
    }
    var seen = {};
    document.querySelectorAll('[data-record-kit]').forEach(function (root) {
      var type = root.getAttribute('data-record-kit');
      var id = root.getAttribute('data-record-id') || location.pathname;
      seen[type] = (seen[type] || 0) + 1;
      var key = 'rk:' + type + ':' + id + (seen[type] > 1 ? ':' + seen[type] : '');
      if (type === 'kuku') kuku(root, key);
      else if (CATS[type]) tally(root, key, type);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
