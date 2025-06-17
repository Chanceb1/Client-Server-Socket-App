<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'

// Reactive data
const mainConsoleContent = ref<string[]>([])
const sideConsoleContent = ref<string[]>([])
const inputText = ref('')
const mainConsoleRef = ref<HTMLElement>()
const sideConsoleRef = ref<HTMLElement>()

// Add content to main console
const addToMainConsole = (text: string) => {
  mainConsoleContent.value.push(`[${new Date().toLocaleTimeString()}] ${text}`)
  nextTick(() => {
    if (mainConsoleRef.value) {
      mainConsoleRef.value.scrollTop = mainConsoleRef.value.scrollHeight
    }
  })
}

// Add content to side console
const addToSideConsole = (text: string) => {
  sideConsoleContent.value.push(`[${new Date().toLocaleTimeString()}] ${text}`)
  nextTick(() => {
    if (sideConsoleRef.value) {
      sideConsoleRef.value.scrollTop = sideConsoleRef.value.scrollHeight
    }
  })
}

// Handle input submission
const handleSubmit = () => {
  if (inputText.value.trim()) {
    const command = inputText.value.trim()
    
    // Add command to main console
    addToMainConsole(`> ${command}`)
    
    // Simple command processing (you can expand this)
    if (command.toLowerCase() === 'clear') {
      mainConsoleContent.value = []
      sideConsoleContent.value = []
    } else if (command.toLowerCase() === 'help') {
      addToMainConsole('Available commands: clear, help, status, info')
    } else if (command.toLowerCase() === 'status') {
      addToSideConsole('System Status: Online')
    } else if (command.toLowerCase() === 'info') {
      addToSideConsole('Socket App Terminal v1.0')
    } else {
      addToMainConsole(`Command not recognized: ${command}`)
      addToSideConsole(`Unknown command: ${command}`)
    }
    
    inputText.value = ''
  }
}

// Handle Enter key press
const handleKeyPress = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    handleSubmit()
  }
}

// Initialize with welcome message
onMounted(() => {
  addToMainConsole('Welcome to Socket App Terminal')
  addToMainConsole('Type "help" for available commands')
  addToSideConsole('Terminal initialized')
})
</script>

<template>
  <div class="terminal-container">
    <!-- Header -->
    <div class="terminal-header">
      <h1>Socket App Console</h1>
    </div>
    
    <!-- Console Areas -->
    <div class="console-wrapper">
      <!-- Main Console (Left, Larger) -->
      <div class="main-console">
        <div class="console-header">
          <span class="console-title">Main Console</span>
        </div>
        <div 
          ref="mainConsoleRef"
          class="console-content"
        >
          <div 
            v-for="(line, index) in mainConsoleContent" 
            :key="index"
            class="console-line"
          >
            {{ line }}
          </div>
        </div>
      </div>
      
      <!-- Side Console (Right, Smaller) -->
      <div class="side-console">
        <div class="console-header">
          <span class="console-title">Status Console</span>
        </div>
        <div 
          ref="sideConsoleRef"
          class="console-content"
        >
          <div 
            v-for="(line, index) in sideConsoleContent" 
            :key="index"
            class="console-line"
          >
            {{ line }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Input Area -->
    <div class="input-area">
      <div class="input-wrapper">
        <span class="prompt">$</span>
        <input
          v-model="inputText"
          @keypress="handleKeyPress"
          type="text"
          class="command-input"
          placeholder="Enter command..."
          autofocus
        />
        <button @click="handleSubmit" class="submit-btn">Send</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.terminal-container {
  width: 100vw;
  height: 100vh;
  background-color: #0a0a0a;
  color: #00ff00;
  font-family: 'Courier New', monospace;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
}

.terminal-header {
  background-color: #1a1a1a;
  padding: 10px 20px;
  border-bottom: 2px solid #00ff00;
  text-align: center;
}

.terminal-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #00ff00;
  text-shadow: 0 0 10px #00ff00;
}

.console-wrapper {
  flex: 1;
  display: flex;
  gap: 10px;
  padding: 10px;
  overflow: hidden;
}

.main-console {
  flex: 3;
  background-color: #111111;
  border: 2px solid #00ff00;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

.side-console {
  flex: 1;
  background-color: #111111;
  border: 2px solid #00ff00;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

.console-header {
  background-color: #1a1a1a;
  padding: 8px 15px;
  border-bottom: 1px solid #00ff00;
  border-radius: 6px 6px 0 0;
}

.console-title {
  font-weight: bold;
  font-size: 0.9rem;
  color: #00ff00;
}

.console-content {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  overflow-x: hidden;
  word-wrap: break-word;
  line-height: 1.4;
}

.console-line {
  margin-bottom: 4px;
  color: #00ff00;
  font-size: 0.85rem;
}

.input-area {
  background-color: #1a1a1a;
  padding: 15px 20px;
  border-top: 2px solid #00ff00;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.prompt {
  color: #00ff00;
  font-weight: bold;
  font-size: 1.1rem;
}

.command-input {
  flex: 1;
  background-color: #0a0a0a;
  border: 1px solid #00ff00;
  color: #00ff00;
  padding: 8px 12px;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  border-radius: 4px;
  outline: none;
}

.command-input:focus {
  border-color: #00ff00;
  box-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
}

.command-input::placeholder {
  color: #666666;
}

.submit-btn {
  background-color: #00ff00;
  color: #000000;
  border: none;
  padding: 8px 16px;
  font-family: 'Courier New', monospace;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover {
  background-color: #00cc00;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}

.submit-btn:active {
  transform: translateY(1px);
}

/* Scrollbar styling */
.console-content::-webkit-scrollbar {
  width: 8px;
}

.console-content::-webkit-scrollbar-track {
  background: #0a0a0a;
}

.console-content::-webkit-scrollbar-thumb {
  background: #00ff00;
  border-radius: 4px;
}

.console-content::-webkit-scrollbar-thumb:hover {
  background: #00cc00;
}

/* Responsive design */
@media (max-width: 768px) {
  .console-wrapper {
    flex-direction: column;
  }
  
  .main-console {
    flex: 2;
  }
  
  .side-console {
    flex: 1;
  }
  
  .input-wrapper {
    flex-direction: column;
    gap: 8px;
  }
  
  .command-input {
    width: 100%;
  }
}
</style>
