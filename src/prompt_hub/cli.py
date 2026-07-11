import json
import sys
import click
from prompt_hub.runner import run_tests

@click.group()
def cli():
    """Prompt-Hub CLI"""
    pass

@cli.command("test")
@click.option("--manifest", default="prompts/manifest.yaml", help="Path to prompt manifest YAML")
@click.option("--provider", default="mock", help="Model provider to use (mock|openai)")
def test(manifest, provider):
    """Run prompt tests from a manifest"""
    results = run_tests(manifest, provider=provider)
    failed = [r for r in results if not r["passed"]]
    print(json.dumps(results, indent=2))
    if failed:
        print(f"{len(failed)} tests failed")
        sys.exit(1)
    print("All prompt tests passed")

@cli.command("serve")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=8501)
def serve(host, port):
    """Start the Streamlit UI"""
    import subprocess
    subprocess.run(["streamlit", "run", "streamlit_app.py", "--server.port", str(port)])

def main():
    cli()

if __name__ == "__main__":
    main()