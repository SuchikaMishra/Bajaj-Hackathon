import email

def extract_email(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)
        body = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body.append(part.get_payload(decode=True).decode('utf-8'))
        else:
            body.append(msg.get_payload(decode=True).decode('utf-8'))
    return [{"heading": None, "clause_number": None, "content": "\n".join(body), "page": None}]
