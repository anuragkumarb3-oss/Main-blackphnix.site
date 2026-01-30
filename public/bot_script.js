                      // Bot Preview UI (Admin Only)
                    const injectBotPreview = () => {
                      if (document.getElementById('bot-preview-container')) return;
                      
                      const userStr = localStorage.getItem('user') || localStorage.getItem('replit_auth');
                      let isAdmin = false;
                      try {
                        const user = JSON.parse(userStr);
                        isAdmin = user && (user.email === 'subhashgupta8971@gmail.com' || user.isAdmin === true);
                      } catch (e) {}

                      if (!isAdmin) return;
                      
                      // Sidebar Menu Item Injection
                      const sidebar = document.querySelector('nav, .sidebar, [role="navigation"]');
                      if (sidebar && !document.getElementById('admin-bot-menu-item')) {
                        const menuItem = document.createElement('div');
                        menuItem.id = 'admin-bot-menu-item';
                        menuItem.style.cssText = 'padding: 10px 20px; cursor: pointer; color: rgba(255,255,255,0.7); display: flex; align-items: center; gap: 10px; transition: all 0.2s;';
                        menuItem.innerHTML = `<span style="font-size: 1.2em;">🤖</span> <span>Bot Console</span>`;
                        menuItem.onmouseover = () => menuItem.style.backgroundColor = 'rgba(147, 51, 234, 0.1)';
                        menuItem.onmouseout = () => menuItem.style.backgroundColor = 'transparent';
                        menuItem.onclick = () => {
                          const panel = document.getElementById('bot-preview-container');
                          if (panel) {
                             panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
                          }
                        };
                        sidebar.appendChild(menuItem);
                      }

                      const container = document.createElement('div');
                      container.id = 'bot-preview-container';
                      container.className = 'glass-effect';
                      container.style.cssText = 'position:fixed; bottom:20px; right:20px; width:300px; padding:15px; border-radius:12px; z-index:1000; font-family:var(--font-mono); font-size:12px; border:1px solid rgba(147, 51, 234, 0.3);';
                      
                      container.innerHTML = `
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom:1px solid rgba(147,51,234,0.2); padding-bottom:5px;">
                          <span style="color:#9333ea; font-weight:bold;">🤖 ADMIN BOT CONSOLE</span>
                          <span id="bot-status-dot" style="width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 5px #10b981;"></span>
                        </div>
                        <div id="bot-logs" style="max-height:150px; overflow-y:auto; color:rgba(255,255,255,0.8);">
                          Loading bot status...
                        </div>
                        <div id="ai-terminal" style="display:none; margin-top:10px; border-top:1px solid rgba(147,51,234,0.3); padding-top:10px;">
                           <div id="ai-proposal" style="background:rgba(0,0,0,0.3); padding:5px; border-radius:4px; margin-bottom:5px; font-size:10px;"></div>
                           <button id="approve-ai-btn" style="width:100%; padding:5px; background:#10b981; border:none; color:white; border-radius:4px; cursor:pointer;">Approve & Execute</button>
                        </div>
                        <div style="display:flex; gap:5px; margin-top:10px;">
                          <button id="test-bot-btn" style="flex:1; padding:5px; background:rgba(147,51,234,0.2); border:1px solid #9333ea; color:white; border-radius:4px; cursor:pointer; font-size:10px;">Test User</button>
                          <button id="self-destruct-btn" style="flex:1; padding:5px; background:rgba(239,68,68,0.2); border:1px solid #ef4444; color:white; border-radius:4px; cursor:pointer; font-size:10px;">Destruct</button>
                        </div>
                      `;
                      
                      document.body.appendChild(container);
                      
                      const updateLogs = async () => {
                        try {
                          const res = await fetch('/api/admin/bot/status');
                          const data = await res.json();
                          const logsDiv = document.getElementById('bot-logs');
                          
                          // Check for errors to trigger AI analysis
                          const latestError = data.last_actions.find(l => l.level === 'ERROR');
                          if (latestError && !window.lastAiIssue) {
                             window.lastAiIssue = latestError.message;
                             const aiRes = await fetch('/api/admin/bot/analyze', {
                               method: 'POST',
                               headers: {'Content-Type': 'application/json'},
                               body: JSON.stringify({issue: latestError.message})
                             });
                             const proposal = await aiRes.json();
                             document.getElementById('ai-terminal').style.display = 'block';
                             document.getElementById('ai-proposal').innerHTML = `<strong>AI Fix:</strong> ${proposal.proposed_fix}<br><strong>Cmds:</strong> ${proposal.commands.join(', ')}`;
                             window.pendingCmds = proposal.commands;
                          }

                          logsDiv.innerHTML = data.last_actions.map(l => `
                            <div style="margin-bottom:5px; border-left:2px solid ${l.level === 'ERROR' ? '#ef4444' : '#9333ea'}; padding-left:5px;">
                              <div style="font-size:10px; opacity:0.6;">${new Date(l.time).toLocaleTimeString()}</div>
                              <div>${l.message}</div>
                            </div>
                          `).join('') || 'No recent actions.';
                        } catch (e) {}
                      };

                      document.getElementById('approve-ai-btn').onclick = async () => {
                        const res = await fetch('/api/admin/bot/approve-fix', {
                          method: 'POST',
                          headers: {'Content-Type': 'application/json'},
                          body: JSON.stringify({commands: window.pendingCmds})
                        });
                        alert('Commands Executed!');
                        document.getElementById('ai-terminal').style.display = 'none';
                        window.lastAiIssue = null;
                        updateLogs();
                      };

                      document.getElementById('test-bot-btn').onclick = async () => {
                        const btn = document.getElementById('test-bot-btn');
                        btn.innerText = 'Creating...';
                        btn.disabled = true;
                        try {
                          const res = await fetch('/api/admin/bot/test-random', { method: 'POST' });
                          const data = await res.json();
                          alert(data.message);
                          updateLogs();
                        } catch (e) {
                          alert('Test failed. Check console.');
                        }
                        btn.innerText = 'Test User';
                        btn.disabled = false;
                      };

                      document.getElementById('self-destruct-btn').onclick = async () => {
                        if(confirm('EMERGENCY: Self-destruct?')) {
                          await fetch('/api/admin/bot/self-destruct', {method: 'POST'});
                          alert('Self-destruct sequence active. Admin notified.');
                        }
                      };

                      setInterval(updateLogs, 5000);
                      updateLogs();
                    };
                    
                    // Inject preview after app loads
                    setTimeout(injectBotPreview, 3000);
                    setInterval(injectBotPreview, 10000);
