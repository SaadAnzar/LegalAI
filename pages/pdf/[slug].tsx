import React, { useState, useEffect, use } from "react";
import { useRouter } from "next/router";
import axios from "axios";
import Chatbot from "../chatbot";

export default function Pdf() {
  const router = useRouter();
  const { slug } = router.query;
  const [summary, setSummary] = useState("");
  const pdfURL =
    `https://firebasestorage.googleapis.com/v0/b/legal-ai-8ebe8.appspot.com/o/pdfs%2` +
    slug +
    "? alt = media";

  useEffect(() => {
    axios.post('http://localhost:5000/summarize', {
      pdfURL: pdfURL
    })
      .then(function (response) {
        console.log(response);
        setSummary(response.data.Summary);
      })
      .catch(function (error) {
        console.log(error);
      });
  }, []);

  return (
    <div className="flex h-screen">
      <div className="w-1/2 h-full">
        <embed
          src={
            `https://firebasestorage.googleapis.com/v0/b/legal-ai-8ebe8.appspot.com/o/pdfs%2` +
            slug +
            "?alt=media"
          }
          type="application/pdf"
          width="100%"
          height="100%"
        ></embed>
      </div>

      <div className="flex w-1/2 p-2 flex-col">
        <div className="flex border-b p-2 w-full">
          <h1 className="font-semibold text-3xl mx-auto">
            Navigating the law. One question at a time.
          </h1>
        </div>

        <p className="p-8">
          {
            summary ? summary : "We are currently processing your document. Please wait a few seconds."
          }
        </p>
        <Chatbot />
      </div>
    </div>
  );
}