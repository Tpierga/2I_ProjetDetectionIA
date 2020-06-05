using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using ConsoleApplication1;

public class testcontroller : MonoBehaviour
{
    public string sIP = "127.0.0.1";
    public int sPort = 50000;
    private UdpSocket server = new UdpSocket();

    void Start()
    {
        server.Start(sIP, sPort, "test", verbose: true);
        Debug.Log("server started");

    }

    void Update()
    {
    }
}
