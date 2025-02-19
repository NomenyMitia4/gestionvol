'use client'
import { format } from "date-fns";
import flightStyle from "./listflight.module.css";
import {useEffect, useRef, useState} from 'react';
import config from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClose, faMessage, faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { faShare } from "@fortawesome/free-solid-svg-icons/faShare";
import { METHODS } from "http";

export default function Flight()
{
    //initate state
    const [flight, setFlight] = useState([]);
    const [message, setMessage] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isChatBotVisible, setIsChatBotVisible] = useState(false);

    const chatContentRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (chatContentRef.current) {
            chatContentRef.current.scrollTop = chatContentRef.current.scrollHeight;
        }
    }, [message]); 
    //Handle Message
    const handleSendMessage = async() => {
        const msg = inputMessage
        setInputMessage(''); 
        if(!inputMessage.trim())
        {
            //empty message
            return;
        }
        try{
            console.log(msg)
            const response = await fetch("http://127.0.0.1:5000/gemini/sendMessage", {
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify({"message": msg})  
            });
            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            // const data = await response.json();
            // console.log("Message sent successfully:", data);

            fetchMessageData();
        
        }catch(error)
        {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again.');
        }
    }

    const fetchMessageData = async() => {
        try{
            const response = await fetch("http://127.0.0.1:5000/gemini/getMessage");
            if(!response.ok)
            {
                throw new Error('Failed to fetch data');
            }
            const data = await response.json();
            setMessage(data);
        }catch(error)
        {
            console.error("Error fetching data: ", error);
        }
    }

    //Fetch data from API
    useEffect(()=>{
        const fetchFlightData = async()=>{
            try{
                const response = await fetch("http://127.0.0.1:5000/flight/getAll");
                if(!response.ok)
                {
                    throw new Error('Failed to fetch data');
                }
                const data = await response.json();
                setFlight(data);
            }catch(error){
                console.error("Error fetching data: ", error);
            }
        };
        fetchMessageData();
        fetchFlightData();
    }, [])

    const toggleChatBot = () => {
        setIsChatBotVisible(!isChatBotVisible);
    };

    const closeChat = () => {
        setIsChatBotVisible(false)
    };

    return(
        <>
        <div className={flightStyle.header}>
            <h1>LIST OF FLIGHTS</h1>
        </div>
        <div className={flightStyle.content}>
            <table border={1} className={flightStyle.flights}>
                <thead>
                    <tr>
                        <td>Airplane</td>
                        <td>Departure Time</td>
                        <td>Destination</td>
                        <td>Origin</td>
                        <td>Distance</td>
                        <td>Price</td>
                        <td>Type</td>
                        <td>Reserved Seat</td>
                    </tr>
                </thead>
                <tbody>
                        {flight.map((f, index) => (
                            <tr key={index}>
                                <td>{f["avion"]["avion_id"]}</td>
                                <td>{format(f["departure_time"], 'yyyy-MMMM-dd HH:mm')}</td>
                                <td>{f["destination"]["city"]}</td>
                                <td>{f["origin"]["city"]}</td>
                                <td>{f["distance"]}</td>
                                <td>{f["price"]}</td>
                                <td>{f["type"]}</td>
                                <td>{f["reserved_seat"]}</td>
                            </tr>
                        ))}
                    </tbody>
            </table>
        </div>
        <div className={flightStyle.chat}>
            <div className={flightStyle.chatBot} id="chatBot" style={{ display: isChatBotVisible ? "block" : "none" }}>   
                        <div className={flightStyle.chatBotBar}>
                            <h3>Personal Assistant</h3>
                            <FontAwesomeIcon icon={faClose} onClick={closeChat} id="closeBar" size="1x"></FontAwesomeIcon>
                        </div>
                        <div className={flightStyle.chatBotContent} ref={chatContentRef}>
                            {
                                message.map((m, index)=>(
                                    m['role'] === "model" ? (
                                        <div key={index} className={flightStyle.chatModel}>
                                          <p>{m['parts']}</p>
                                        </div>
                                      ) : (
                                        <div key={index} className={flightStyle.chatUser}>
                                          <p>{m['parts']}</p>
                                        </div>
                                    ))
                                )
                            }
                        </div>
                        <div className={flightStyle.chatBotFooter}>
                            <input type="text" value={inputMessage} onChange={(e)=> setInputMessage(e.target.value)} onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    handleSendMessage(); // Send message when Enter is pressed
                                }
                            }}/>
                            <FontAwesomeIcon icon={faPaperPlane} onClick={handleSendMessage} size="1x"></FontAwesomeIcon>
                        </div>
            </div>
            <div className={flightStyle.chatIcon} style={{ display: isChatBotVisible ? "none" : "block"}}>
                <button style={{ cursor:"pointer"}}>
                    <FontAwesomeIcon icon={faMessage} id="chatIcon" size="2x" onClick={toggleChatBot} ></FontAwesomeIcon>
                </button>
            </div>
        </div>
        </>
    )
}