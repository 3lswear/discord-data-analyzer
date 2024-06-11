const output = document.getElementById("output");
function addToOutput(s) {
	output.value += s + "\n";
}

if (typeof(showDirectoryPicker) == "undefined"){
	errorStr = "Your browser is not supported! Please open in chrome or a recent chromium-based browser!";
	alert(errorStr);
	addToOutput(errorStr);
}

addToOutput("Loading python packages... 🔧");
// init Pyodide
async function main() {
	var out2 = document.getElementById("output2")
	let pyodide = await loadPyodide({
		stdout: (text) => {out2.textContent += text + "\n";},
		stderr: (text) => {out2.textContent += text + "\n";}
	});
	await pyodide.loadPackage("micropip");
	const micropip = pyodide.pyimport("micropip");
	await micropip.install("matplotlib");
	// await micropip.install("pandas");
	addToOutput("Python packages and runtime loaded! ✅");
	document.getElementById("directory-picker").removeAttribute("disabled")
	document.getElementById("logo").style.filter = "none";
	document.getElementById("overlay").style.display = "none";
	return pyodide;
}
let pyodideReadyPromise = main();


async function evaluatePython() {
	let pyodide = await pyodideReadyPromise;
	try {
		const dirHandle = await showDirectoryPicker();
		const permissionStatus = await dirHandle.requestPermission({
			mode: "read",
		});

		if (permissionStatus !== "granted") {
			throw new Error("read access to directory not granted");
		}

		const nativefs = await pyodide.mountNativeFS("/data", dirHandle);
		addToOutput("Loading the python script... 🔧");
		pyodide.runPython(await (await fetch("/main.py")).text())
		addToOutput("Python file loaded! ✅");
		document.getElementById("runbutton").removeAttribute("disabled")

	} catch (err) {
		addToOutput(err);
	}
}



