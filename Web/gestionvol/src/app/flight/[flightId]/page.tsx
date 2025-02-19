export default function FlightDetails({params,}: {
    params:{flightId:string};
})
{
    return(
        <>
            <h1>Flight Details</h1>
            <p>{params.flightId}</p>
        </>
    )
}