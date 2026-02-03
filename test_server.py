#!/usr/bin/env python3
"""Quick test for the Arabic Accents MCP server."""

import json
import subprocess
import sys

def test_server():
    # Start server as subprocess
    proc = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    
    def send(msg):
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()
        line = proc.stdout.readline()
        return json.loads(line) if line else None
    
    print("=" * 50)
    print("Testing Arabic Accents MCP Server")
    print("=" * 50)
    
    # Test 1: Initialize
    print("\n1. Initialize...")
    resp = send({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    })
    if resp and "result" in resp:
        print(f"   OK - Server: {resp['result']['serverInfo']['name']} v{resp['result']['serverInfo']['version']}")
    else:
        print(f"   FAIL - {resp}")
        return False
    
    # Send initialized notification
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
    proc.stdin.flush()
    
    # Test 2: List resources
    print("\n2. List resources...")
    resp = send({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "resources/list",
        "params": {}
    })
    if resp and "result" in resp:
        resources = resp["result"].get("resources", [])
        print(f"   OK - Found {len(resources)} resource(s):")
        for r in resources:
            print(f"      - {r.get('name', r.get('uri'))}")
    else:
        print(f"   FAIL - {resp}")
    
    # Test 3: List tools
    print("\n3. List tools...")
    resp = send({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/list",
        "params": {}
    })
    if resp and "result" in resp:
        tools = resp["result"].get("tools", [])
        print(f"   OK - Found {len(tools)} tool(s):")
        for t in tools:
            print(f"      - {t.get('name')}")
    else:
        print(f"   FAIL - {resp}")
    
    # Test 4: Call list_available_accents tool
    print("\n4. Call list_available_accents tool...")
    resp = send({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "list_available_accents",
            "arguments": {}
        }
    })
    if resp and "result" in resp:
        content = resp["result"].get("content", [])
        if content:
            text = content[0].get("text", "")
            print(f"   OK - Response preview:")
            for line in text.split("\n")[:5]:
                print(f"      {line}")
    else:
        print(f"   FAIL - {resp}")
    
    # Test 5: Read a resource
    print("\n5. Read emirati resource...")
    resp = send({
        "jsonrpc": "2.0",
        "id": 5,
        "method": "resources/read",
        "params": {"uri": "arabic-accents://emirati"}
    })
    if resp and "result" in resp:
        contents = resp["result"].get("contents", [])
        if contents:
            text = contents[0].get("text", "")
            print(f"   OK - Content length: {len(text)} chars")
            # Show preview (ASCII-safe for Windows console)
            preview = text[:200].encode('ascii', 'replace').decode('ascii')
            print(f"   Preview: {preview}...")
    else:
        print(f"   FAIL - {resp}")
    
    # Cleanup
    proc.terminate()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_server()
