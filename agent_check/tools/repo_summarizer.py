from transformers import pipeline
import os
class RepoSumm:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    def read_repo_code(self,directory):
        content = ""
        for root,_,files in os.walk(directory):
            for file in files:
                if file.endswith((".html")):
                    path = os.path.join(root,file)
                    try:
                        with open(path, "r",errors="ignore") as f:
                            content+= f.read()+"\n"
                    except Exception as e:
                        print("Skipped")
        return content
    def chunk(self,text,maxlen = 1024):
        """Breaks long sentences"""
        sentences = text.split(".")
        chunks = []
        current = ""
        for sent in sentences:
            if len(current) + len(sent) < maxlen:
                current+= sent+"."
            elif current:
                chunks.append(sent)
                current = sent +"."
        if current:
            chunks.append(current)
        return chunks
    def repo_sum(self, directory):
        print("Reading repo files...")
        code_text = self.read_repo_code(directory)
        print("Chunking...")
        # print(code_text)
        chunks = self.chunk(code_text)
        print(f"🔍 Created {len(chunks)} chunks")
        for i, c in enumerate(chunks[:3], 1):
            print(f"\n--- Chunk {i} ---\n{c[:300]}...")

        print("Summarizing...")
        summaries = []
        for chunk in chunks:
            num_tokens = len(chunk.split())

            if num_tokens < 20:
                continue
            if num_tokens > 1000:
                chunk = " ".join(chunk.split()[:1000])
                num_tokens = 1000
            max_len = min(50,num_tokens//2)
            min_len = min(25,max_len//2)

            try:
                summary = self.summarizer(
                    chunk,
                    max_length=max_len,
                    min_length=min_len,
                    truncation=True,
                    do_sample=False
                )[0]["summary_text"]
                summaries.append(summary)
            except Exception as e:
                print(f"exception during {e}")
        final_summary = "\n".join(summaries)
        return final_summary

