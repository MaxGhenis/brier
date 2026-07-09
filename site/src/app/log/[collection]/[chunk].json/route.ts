import {
  buildThesisLogChunk,
  isThesisLogChunkCollection,
  THESIS_LOG_CHUNK_SIZE,
} from "@/data/thesis-log";
import { loadThesisLogData } from "@/data/thesis-log-runtime";

export const dynamic = "force-static";

interface ThesisLogChunkRouteContext {
  params: Promise<{}>;
}

export async function GET(
  request: Request,
  _context: ThesisLogChunkRouteContext,
) {
  const { collection, chunk } = getCollectionAndChunk(request.url);
  if (!isThesisLogChunkCollection(collection)) {
    return Response.json(
      { error: "unknown_thesis_log_collection", collection },
      { status: 404 },
    );
  }

  const chunkIndex = Number(chunk);
  const data = await loadThesisLogData();
  const chunkCount = Math.ceil(data[collection].length / THESIS_LOG_CHUNK_SIZE);
  if (
    !Number.isInteger(chunkIndex) ||
    chunkIndex < 0 ||
    chunkIndex >= chunkCount
  ) {
    return Response.json(
      { error: "unknown_thesis_log_chunk", collection, chunk },
      { status: 404 },
    );
  }

  return Response.json(buildThesisLogChunk(data, collection, chunkIndex));
}

function getCollectionAndChunk(url: string) {
  const segments = new URL(url).pathname.split("/").filter(Boolean);
  return {
    chunk: segments.at(-1)?.replace(/(\.json)+$/, "") ?? "",
    collection: segments.at(-2) ?? "",
  };
}
