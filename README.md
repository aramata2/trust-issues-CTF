# Trust Issues 🔒
**CTF Challenge | Category: Web Exploitation | Difficulty: Easy-Medium | Points: 150**

> *"Our developer learned their lesson about plaintext cookies. This time they encoded everything. Totally safe now, right?"*

---

## Challenge Description

Players are presented with a simple employee login portal. After logging in, the server assigns a cookie to track their role. The cookie looks like scrambled nonsense — but it's actually just Base64 encoding. The goal is to decode it, change the role from `user` to `admin`, re-encode it, and swap it back in. The server trusts the cookie blindly and will hand over the flag.

**Flag:** `CTF{enc0d1ng_1s_n0t_encryp710n}`

**Login credentials (given to players):** `player` / `password123`

**Estimated solve time for beginners:** 15–25 minutes

---

## Intended Solve Path

1. Log in with the provided credentials
2. Open browser DevTools → Application → Cookies
3. Notice the `role` cookie value (e.g. `dXNlcg==`) — recognize Base64 by the `==` padding
4. Decode it: `dXNlcg==` → `user`
5. Encode `admin` in Base64: `YWRtaW4=`
6. Replace the cookie value with `YWRtaW4=` and refresh
7. Profit 🏁

---

## Running Locally (for testing)

### Option 1 — Docker Compose (recommended)
```bash
docker-compose up --build
```
Visit `http://localhost:5000`

### Option 2 — Plain Python
```bash
pip install -r requirements.txt
python app.py
```
Visit `http://localhost:5000`

---

## Deploying on a VM

```bash
# Clone the repo
git clone <your-repo-url>
cd trust-issues

# Build and run with Docker
docker-compose up -d --build

# The challenge will be live on port 5000
```

To expose on a different port, edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"   # host_port:container_port
```

---

## File Structure

```
trust-issues/
├── app.py                  # Flask application
├── templates/
│   ├── login.html          # Login page
│   └── dashboard.html      # Dashboard (shows flag if admin)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Hints (for CTFd or similar platforms)

| # | Cost | Hint |
|---|------|------|
| 1 | 15 pts | *"The cookie value looks a little scrambled. What encoding ends with `==`?"* |
| 2 | 30 pts | *"CyberChef is your friend."* |

---

## Author Notes

The vulnerability is intentional — the server blindly trusts the `role` cookie without any signing or integrity check. The lesson: **encoding is not encryption**. Just because something looks scrambled doesn't mean it's protected.
