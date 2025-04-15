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

            let output = result.output;

            // If the output is a string that looks like an array, fix the quotes and parse it
            if (typeof output === 'string') {
                // Replace single quotes with double quotes for valid JSON
                const fixedOutput = output.replace(/'/g, '"');

                try {
                    // Try to parse the corrected string into an actual array
                    output = JSON.parse(fixedOutput);
                } catch (error) {
                    setOutput(`Error parsing output: ${error.message}`);
                    return;
                }
            }

            // Now, handle output if it's an array
            if (Array.isArray(output)) {
                const formattedOutput = formatOutput(output);
                setOutput(formattedOutput);
            } else {
                setOutput(`Error: Expected an array, but got: ${typeof output}`);
            }
        } catch (error) {
            console.error('Error executing code:', error);
            setOutput(`Error: ${error.message || 'Failed to execute code'}`);
        }
    };


    const formatOutput = (output) => {
        // Check if output is an array before applying .map()
        if (Array.isArray(output)) {
            const formattedCode = output.map(instruction => {
                return `${instruction.raw}`;
            }).join('\n');

            return `\`\`\`assembly\n${formattedCode}\n\`\`\``;
        } else {
            return 'No valid output format received';
        }
    };


    const handleReset = () => {
        setCode(initialCode);
        setOutput('');
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

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="space-y-4">
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

                        <div className="space-y-4">
                            <h2 className="text-2xl font-medium">Output</h2>
                            <div
                                className="h-[600px] bg-secondary/50 rounded-lg p-6 font-mono text-sm overflow-auto border shadow-sm"
                                style={{whiteSpace: 'pre-wrap', wordWrap: 'break-word'}}
                            >
                                <code>{output || 'Program output will appear here...'}</code>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </TooltipProvider>
    );
}

export default App;