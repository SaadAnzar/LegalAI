import React, { useState, useEffect } from 'react'
import Layout from './layout';
import { Toaster, toast } from 'react-hot-toast';
import { storage } from '../config/firebase';
import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import axios from 'axios';
import { useRouter } from 'next/router';

export default function Upload() {
    const [file, setFile] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleSubmit = (e: any) => {
        e.preventDefault();
        console.log(file);
        // Create a root reference
        const storageRef = ref(storage, 'pdfs/' + file.name + Date.now());

        // Upload file and metadata to the object 'images/mountains.jpg'
        const uploadTask = uploadBytesResumable(storageRef, file);

        // Listen for state changes, errors, and completion of the upload.
        uploadTask.on('state_changed', (snapshot) => {
            // Get task progress, including the number of bytes uploaded and the total number of bytes to be uploaded
            const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            console.log('Upload is ' + progress + '% done');
            switch (snapshot.state) {
                case 'paused':
                    console.log('Upload is paused');
                    break;
                case 'running':
                    console.log('Upload is running');
                    break;
            }
        }
            , (error) => {
                // A full list of error codes is available at
                // https://firebase.google.com/docs/storage/web/handle-errors
                switch (error.code) {
                    case 'storage/unauthorized':
                        // User doesn't have permission to access the object
                        break;
                    case 'storage/canceled':
                        // User canceled the upload
                        break;

                    // ...

                    case 'storage/unknown':
                        // Unknown error occurred, inspect error.serverResponse
                        break;
                }
            }
            , () => {
                // Upload completed successfully, now we can get the download URL
                getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
                    console.log('File available at', downloadURL);
                    toast.success('File uploaded successfully!');
                    console.log(downloadURL.replace('https://firebasestorage.googleapis.com/v0/b/legal-ai-8ebe8.appspot.com/o', ''));

                    toast.loading('Processing your document...');
                    
                    axios.post('http://localhost:8800/pdf', {

                        pdfURL: downloadURL
                    })
                        .then(function (response) {
                            console.log(response);
                            setTimeout(() => {
                                toast.success('Your document is ready!');
                            }, 3000);

                            router.push(`/pdf/${downloadURL.replace('https://firebasestorage.googleapis.com/v0/b/legal-ai-8ebe8.appspot.com/o/pdfs%2', '')}`);
                            setLoading(false);
                        })
                        .catch(function (error) {
                            console.log(error);
                            setLoading(false);
                        });
                });
            }
        );
    }

    const handleChange = (e: any) => {
        if (e.target.files[0].type == 'application/pdf') {
            setFile(e.target.files[0]);
        } else {
            // alert('Please upload a pdf file');
            setFile(e.target.files[0]);
        }
    }

    return (
        <Layout>
            <div><Toaster /></div>
            <main className='h-screen flex items-center justify-center'>
                <div className='flex flex-col p-2 items-center gap-y-4'>
                    <h2 className='text-2xl'>
                        Upload your document
                    </h2>

                    {/* a form with styles for user to upload pdf */}
                    <form className='flex flex-col items-center gap-y-4' onSubmit={handleSubmit}>
                        <input type='file' onChange={handleChange} className='bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded' />

                        {
                            file && (
                                <button
                                    type='submit'
                                    className='flex items-center gap-x-2 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded'>
                                    <span>Upload</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                    </svg>
                                </button>)
                        }
                    </form>
                </div>

                {/* show loading spinner when processing pdf */}
                {
                    loading && (
                        <div className='flex flex-col items-center gap-y-4'>
                            <svg className="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v1a7 7 0 00-7 7h1zm0 0a8 8 0 018 8H9a7 7 0 00-7-7v1zm0 0h1a8 8 0 018 8v-1a7 7 0 00-7-7zm0 0v1a8 8 0 01-8-8h1a7 7 0 007 7z"></path>
                            </svg>
                            <p className='text-xl'>Processing your document...</p>
                        </div>
                    )
                }

            </main>
        </Layout>
    )
}