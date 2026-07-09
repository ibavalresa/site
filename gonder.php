<?php
// İletişim formu → e-posta gönderimi (İBAVALRESA)
header('Content-Type: application/json; charset=utf-8');

// Yalnızca POST
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Yalnızca POST istekleri kabul edilir.']);
    exit;
}

// Honeypot: gizli "website" alanı doluysa bot kabul et, sessizce başarı dön
if (!empty($_POST['website'])) {
    echo json_encode(['ok' => true]);
    exit;
}

// Yardımcılar
function field($k) { return trim((string)($_POST[$k] ?? '')); }
// Başlık enjeksiyonuna karşı: satır sonlarını temizle
function header_safe($s) { return trim(str_replace(["\r", "\n", "%0a", "%0d", "\0"], '', $s)); }

$name    = field('name');
$company = field('company');
$email   = field('email');
$phone   = field('phone');
$subject = field('subject');
$message = field('message');
$consent = field('consent');

// Sunucu tarafı doğrulama
$errors = [];
if ($name === '')                                                  $errors[] = 'name';
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL))   $errors[] = 'email';
if ($subject === '')                                               $errors[] = 'subject';
if ($message === '')                                               $errors[] = 'message';
if ($consent === '')                                               $errors[] = 'consent';

if ($errors) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'Lütfen zorunlu alanları doldurun.', 'fields' => $errors]);
    exit;
}

// Basit uzunluk sınırı
if (mb_strlen($message) > 5000) $message = mb_substr($message, 0, 5000);

// Alıcı
$to = 'info@ibavalresa.com.tr';

// Gönderen alan adı (host'tan; www. atılır)
$fromDomain = preg_replace('/^www\./', '', $_SERVER['HTTP_HOST'] ?? 'ibavalresa.com.tr');
$fromDomain = header_safe($fromDomain) ?: 'ibavalresa.com.tr';
$fromAddr   = 'no-reply@' . $fromDomain;

// Konu (Türkçe için UTF-8/Base64 kodlanır)
$mailSubject    = 'İletişim Formu: ' . $subject;
$encodedSubject = '=?UTF-8?B?' . base64_encode($mailSubject) . '?=';

// Gövde
$body  = "Yeni iletişim formu mesajı\n";
$body .= "----------------------------------------\n";
$body .= "Ad Soyad : {$name}\n";
$body .= "Firma    : " . ($company !== '' ? $company : '-') . "\n";
$body .= "E-posta  : {$email}\n";
$body .= "Telefon  : " . ($phone !== '' ? $phone : '-') . "\n";
$body .= "Konu     : {$subject}\n";
$body .= "----------------------------------------\n";
$body .= "Mesaj:\n{$message}\n";
$body .= "----------------------------------------\n";
$body .= "Tarih : " . date('d.m.Y H:i') . "\n";
$body .= "IP    : " . ($_SERVER['REMOTE_ADDR'] ?? '-') . "\n";

// Başlıklar (Reply-To kullanıcının adresi olur → doğrudan yanıtlanabilir)
$replyName  = header_safe($name);
$replyEmail = header_safe($email);
$headers  = "From: İbavalresa Web <{$fromAddr}>\r\n";
$headers .= "Reply-To: {$replyName} <{$replyEmail}>\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";

// Gönder (bazı sunucular -f envelope sender ister)
$sent = @mail($to, $encodedSubject, $body, $headers, '-f ' . $fromAddr);

if ($sent) {
    echo json_encode(['ok' => true]);
} else {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Mesaj gönderilemedi. Lütfen daha sonra tekrar deneyin.']);
}
