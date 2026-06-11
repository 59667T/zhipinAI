const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');

const allJS = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g).join('');
const opens = (allJS.match(/\{/g) || []).length;
// Count close braces differently to avoid escape issues
let closeCount = 0;
for (let i = 0; i < allJS.length; i++) {
    if (allJS[i] === '}') closeCount++;
}
console.log('Open braces:', opens, 'Close braces:', closeCount, 'Match:', opens === closeCount);

const jobMatches = html.match(/\{id:(\d+),title:/g) || [];
console.log('Job count in buildAllJobs:', jobMatches.length);

const ids = jobMatches.map(m => { const r = m.match(/id:(\d+)/); return r ? parseInt(r[1]) : 0; });
console.log('Job IDs:', ids.join(', '));

const missing = [];
for (let i = 26; i <= 47; i++) {
    if (!ids.includes(i)) missing.push(i);
}
console.log('Missing IDs (26-47):', missing.length > 0 ? missing.join(',') : 'NONE - all present');

// Verify old job interviews
const intvIds = [];
const intvRe = /^\s*(\d+):/gm;
let im;
while ((im = intvRe.exec(html)) !== null) {
    intvIds.push(parseInt(im[1]));
}
console.log('Interview IDs:', intvIds.join(', '));
const missingIntv = [];
for (let i = 26; i <= 47; i++) {
    if (!intvIds.includes(i)) missingIntv.push(i);
}
console.log('Missing Interview IDs (26-47):', missingIntv.length > 0 ? missingIntv.join(',') : 'NONE - all present');

console.log('\n=== VALIDATION ===');
console.log('Brace match:', opens === closeCount ? 'PASS' : 'FAIL');
console.log('Jobs 26-47:', missing.length === 0 ? 'PASS' : 'FAIL - missing: ' + missing.join(','));
console.log('Interviews 26-47:', missingIntv.length === 0 ? 'PASS' : 'FAIL');
