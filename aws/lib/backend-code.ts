import { execFileSync } from 'node:child_process';
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as lambda from 'aws-cdk-lib/aws-lambda';

const BACKEND_DIR = path.resolve(__dirname, '..', '..', 'backend');
const BUILD_DIR = path.resolve(__dirname, '..', '.build');
const BUNDLE_DIR = path.join(BUILD_DIR, 'lambda');
const REQUIREMENTS = path.join(BUILD_DIR, 'requirements.txt');

// Must match `architecture` in bin/aws.ts and the runtime's Python version:
// this is what decides which wheels uv downloads.
const PYTHON_VERSION = '3.13';
const PYTHON_PLATFORM = 'aarch64-manylinux2014';

// Everything the Lambda imports, flat modules the way the api container runs
// them. build_content.py is deliberately absent: it generates the static
// content, which the deploy script ships to S3 — the API never serves it.
const MODULES = ['db.py', 'lambda_handler.py', 'server.py', 'ulid.py', 'user.py'];

function uv(args: string[]): void {
  try {
    execFileSync('uv', args, { cwd: BACKEND_DIR, stdio: ['ignore', 'ignore', 'inherit'] });
  } catch (e) {
    throw new Error(
      `\`uv ${args.join(' ')}\` failed. The Lambda bundle is built from ` +
      `backend/uv.lock with uv (https://docs.astral.sh/uv/), the same tool ` +
      `backend/Dockerfile.dev installs from. Install it and retry.\n${e}`
    );
  }
}

/**
 * The FastAPI app packaged for Lambda: backend/uv.lock's dependencies plus the
 * modules above, in one directory.
 *
 * Built on the host rather than in a Docker bundling image. uv resolves wheels
 * for a platform it is not running on, so `--python-platform` gets Linux/ARM
 * wheels from a Mac without a container in the loop — and the versions come
 * from uv.lock, so the Lambda runs exactly what `docker compose up` runs.
 * Anything not shipping a matching wheel would fail loudly here rather than at
 * import time in AWS.
 */
export function backendLambdaCode(): lambda.Code {
  fs.rmSync(BUNDLE_DIR, { recursive: true, force: true });
  fs.mkdirSync(BUNDLE_DIR, { recursive: true });

  // --no-emit-project: the backend is `package = false`, so there is no project
  // wheel to install — only its dependencies. --no-hashes because the hashes
  // would pin the *resolution*, and this one deliberately re-resolves onto
  // another platform.
  uv([
    'export', '--frozen', '--no-dev', '--no-emit-project', '--no-hashes',
    '--quiet', '-o', REQUIREMENTS,
  ]);
  uv([
    'pip', 'install', '--quiet', '-r', REQUIREMENTS, '--target', BUNDLE_DIR,
    '--python-version', PYTHON_VERSION, '--python-platform', PYTHON_PLATFORM,
  ]);

  for (const m of MODULES) {
    fs.copyFileSync(path.join(BACKEND_DIR, m), path.join(BUNDLE_DIR, m));
  }

  return lambda.Code.fromAsset(BUNDLE_DIR);
}
