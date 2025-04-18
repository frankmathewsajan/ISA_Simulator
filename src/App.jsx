import {useState} from 'react';
import Editor from '@monaco-editor/react';
import {Code2, Play, RotateCcw} from 'lucide-react';
import {Button} from './components/ui/button';
import {Tooltip, TooltipContent, TooltipProvider, TooltipTrigger} from './components/ui/tooltip';

const initialCode =
    `MOV AX, 5`;

const monacoTheme = {
    base: 'vs',
    inherit: true,
    rules: [
        {token: 'comment', foreground: '8b949e', fontStyle: 'italic'},
        {token: 'keyword', foreground: 'ff7b72', fontStyle: 'bold'},
        {token: 'string', foreground: '79c0ff'},
        {token: 'number', foreground: 'd2a8ff'},
        {token: 'delimiter', foreground: '8b949e'},
        {token: 'type', foreground: '79c0ff'},
        {token: 'identifier', foreground: 'ffa657'},
    ],
    colors: {
        'editor.background': '#fdfcfa',
        'editor.foreground': '#24292e',
        'editor.lineHighlightBackground': '#f6f5f4',
        'editorLineNumber.foreground': '#8b949e',
        'editorCursor.foreground': '#24292e',
        'editor.selectionBackground': '#dddbd740',
        'editor.inactiveSelectionBackground': '#dddbd720',
        'editor.selectionHighlightBackground': '#dddbd730',
    },
};

function App() {
    const [code, setCode] = useState(initialCode);
    const [output, setOutput] = useState('');
    const [cpuState, setCpuState] = useState(null);
    const [memory, setMemory] = useState(null);

    const handleEditorChange = (value) => {
        if (value) setCode(value);
    };

    const handleRun = async () => {
        try {
            setOutput('Running code...');

            const response = await fetch('http://127.0.0.1:5000/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({code}),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Backend Response:', result);

            if (result.error) {
                setOutput(`
                    <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
                        <div class="font-medium mb-1">Error:</div>
                        <pre class="whitespace-pre-wrap">${result.error}</pre>
                    </div>
                `);
                return;
            }

            // Update CPU state and memory
            setCpuState(result.cpu_state);
            setMemory(result.memory);

            // Format the output
            const formattedOutput = formatOutput(code, result);
            setOutput(formattedOutput);
        } catch (error) {
            console.error('Error executing code:', error);
            setOutput(`Error: ${error.message || 'Failed to execute code'}`);
        }
    };

    const formatOutput = (code, result) => {
        const sections = [];
    
        // Code section with light terminal styling
        sections.push(`
            <div class="mb-6 bg-gray-50 p-4 rounded-lg text-gray-800 font-mono border">
                <div class="flex items-center mb-2 text-xs text-gray-500">
                    <span>$ assembly_execution.asm</span>
                </div>
                <pre class="font-mono">${code}</pre>
            </div>
        `);
    
        if (result.cpu_state) {
            sections.push(`
                <div class="bg-white p-4 rounded-lg mb-6 border">
                    <div class="grid grid-cols-2 gap-4">
                        <!-- First Row: General Purpose Registers and Flags -->
                        <div class="col-span-1">
                            <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden">
                                <thead>
                                    <tr class="bg-blue-50">
                                        <th class="p-3 text-blue-700 font-mono text-left" colspan="4">General Purpose Registers</th>
                                    </tr>
                                </thead>
                                <tbody class="text-gray-700">
                                    <tr>
                                        <td class="p-3 border-t">AX: 0x${result.cpu_state.AX?.toString(16).padStart(4, '0') || '0000'}</td>
                                        <td class="p-3 border-t">BX: 0x${result.cpu_state.BX?.toString(16).padStart(4, '0') || '0000'}</td>
                                    </tr>
                                    <tr>
                                        <td class="p-3 border-t">CX: 0x${result.cpu_state.CX?.toString(16).padStart(4, '0') || '0000'}</td>
                                        <td class="p-3 border-t">DX: 0x${result.cpu_state.DX?.toString(16).padStart(4, '0') || '0000'}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="col-span-1">
                            <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden">
                                <thead>
                                    <tr class="bg-red-50">
                                        <th class="p-3 text-red-700 font-mono text-left" colspan="4">CPU Flags</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td class="p-3 border-t">
                                            <div class="flex items-center gap-2">
                                                <div class="${result.cpu_state.ZF ? 'bg-green-500' : 'bg-gray-300'} w-3 h-3 rounded-full"></div>
                                                <span class="text-gray-700">ZF</span>
                                            </div>
                                        </td>
                                        <td class="p-3 border-t">
                                            <div class="flex items-center gap-2">
                                                <div class="${result.cpu_state.CF ? 'bg-green-500' : 'bg-gray-300'} w-3 h-3 rounded-full"></div>
                                                <span class="text-gray-700">CF</span>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="p-3 border-t">
                                            <div class="flex items-center gap-2">
                                                <div class="${result.cpu_state.SF ? 'bg-green-500' : 'bg-gray-300'} w-3 h-3 rounded-full"></div>
                                                <span class="text-gray-700">SF</span>
                                            </div>
                                        </td>
                                        <td class="p-3 border-t">
                                            <div class="flex items-center gap-2">
                                                <div class="${result.cpu_state.OF ? 'bg-green-500' : 'bg-gray-300'} w-3 h-3 rounded-full"></div>
                                                <span class="text-gray-700">OF</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <!-- Second Row: Segment and Index Registers -->
                        <div class="col-span-1">
                            <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden">
                                <thead>
                                    <tr class="bg-purple-50">
                                        <th class="p-3 text-purple-700 font-mono text-left" colspan="2">Segment Registers</th>
                                    </tr>
                                </thead>
                                <tbody class="text-gray-700">
                                    <tr>
                                        <td class="p-2 border-t">CS: 0x${result.cpu_state.CS?.toString(16).padStart(4, '0') || '0000'}</td>
                                        <td class="p-2 border-t">DS: 0x${result.cpu_state.DS?.toString(16).padStart(4, '0') || '0000'}</td>
                                    </tr>
                                    <tr>
                                        <td class="p-2 border-t">SS: 0x${result.cpu_state.SS?.toString(16).padStart(4, '0') || '0000'}</td>
                                        <td class="p-2 border-t">ES: 0x${result.cpu_state.ES?.toString(16).padStart(4, '0') || '0000'}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="col-span-1">
                            <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden">
                                <thead>
                                    <tr class="bg-cyan-50">
                                        <th class="p-3 text-cyan-700 font-mono text-left" colspan="2">Index Registers</th>
                                    </tr>
                                </thead>
                                <tbody class="text-gray-700">
                                    <tr>
                                        <td class="p-2 border-t">SI: 0x${result.cpu_state.SI?.toString(16).padStart(4, '0') || '0000'}</td>
                                        <td class="p-2 border-t">DI: 0x${result.cpu_state.DI?.toString(16).padStart(4, '0') || '0000'}</td>
                                    </tr>
                                    <tr>
                                        <td class="p-2 border-t">BP: 0x${result.cpu_state.BP?.toString(16).padStart(4, '0') || '0000'}</td>
                                        <td class="p-2 border-t">SP: 0x${result.cpu_state.SP?.toString(16).padStart(4, '0') || '0000'}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            `);
        }
    
        if (result.memory) {
            sections.push(`
                <div class="bg-white p-4 rounded-lg border">
                    <table class="w-full border-collapse bg-gray-50 rounded-lg overflow-hidden">
                        <thead>
                            <tr class="bg-amber-50">
                                <th class="p-3 text-amber-700 font-mono text-left" colspan="2">Memory Monitor</th>
                            </tr>
                            <tr class="bg-gray-100">
                                <th class="p-2 text-gray-600 text-left">Address</th>
                                <th class="p-2 text-gray-600 text-left">Value</th>
                            </tr>
                        </thead>
                        <tbody class="text-gray-700">
                            ${Object.entries(result.memory)
                                .map(([address, value]) => `
                                    <tr>
                                        <td class="p-2 border-t">${address}</td>
                                        <td class="p-2 border-t">0x${value.toString(16).padStart(4, '0')}</td>
                                    </tr>
                                `).join('')}
                        </tbody>
                    </table>
                </div>
            `);
        }
    
        return sections.join('');
    };

    const handleReset = () => {
        setCode(initialCode);
        setOutput('');
        setCpuState(null);
        setMemory(null);
    };

    return (
        <TooltipProvider>
            <div className="min-h-screen bg-background">
                <div className="container py-8 space-y-8">
                    <header className="space-y-2">
                        <div className="flex items-center gap-2">
                            <Code2 className="h-8 w-8"/>
                            <h1 className="text-4xl font-semibold tracking-tight">Assembly IDE</h1>
                        </div>
                        <p className="text-muted-foreground text-lg">
                            Write and simulate assembly code directly in your browser
                        </p>
                    </header>

                    <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                        <div className="space-y-4 lg:col-span-2">
                            <div className="flex items-center justify-between">
                                <h2 className="text-2xl font-medium">Editor</h2>
                                <div className="flex gap-3">
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={handleReset}
                                                className="h-9 px-4"
                                            >
                                                <RotateCcw className="h-4 w-4 mr-2"/>
                                                Reset
                                            </Button>
                                        </TooltipTrigger>
                                        <TooltipContent>Reset to initial code</TooltipContent>
                                    </Tooltip>

                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Button
                                                size="sm"
                                                onClick={handleRun}
                                                className="h-9 px-4"
                                            >
                                                <Play className="h-4 w-4 mr-2"/>
                                                Run
                                            </Button>
                                        </TooltipTrigger>
                                        <TooltipContent>Execute the code</TooltipContent>
                                    </Tooltip>
                                </div>
                            </div>
                            <div className="h-[600px] rounded-lg overflow-hidden border shadow-sm">
                                <Editor
                                    height="100%"
                                    defaultLanguage="nasm"
                                    theme={monacoTheme}
                                    value={code}
                                    onChange={handleEditorChange}
                                    options={{
                                        minimap: {enabled: false},
                                        fontSize: 14,
                                        lineNumbers: 'on',
                                        roundedSelection: false,
                                        scrollBeyondLastLine: false,
                                        readOnly: false,
                                        automaticLayout: true,
                                        padding: {top: 16, bottom: 16},
                                        fontFamily: "'JetBrains Mono', 'SF Mono', Menlo, Monaco, 'Courier New', monospace",
                                        fontLigatures: true,
                                    }}
                                />
                            </div>
                        </div>

                        <div className="space-y-4 lg:col-span-3">
                            <h2 className="text-2xl font-medium">CPU Monitor</h2>
                            <div
                                className="h-[600px] bg-white rounded-lg p-6 font-mono text-sm overflow-auto border shadow-sm"
                                dangerouslySetInnerHTML={{ __html: output || '<div class="text-gray-400">CPU monitor initializing...</div>' }}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </TooltipProvider>
    );
}

export default App;