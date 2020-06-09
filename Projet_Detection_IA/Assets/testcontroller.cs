using System.Collections.Generic;
using UnityEngine;
using ConsoleApplication1;
using Newtonsoft.Json;
using System.IO;

public class testcontroller : MonoBehaviour
{
    private static readonly string ServerPath = Application.persistentDataPath;
    public string sIP = "127.0.0.1";
    public int sPort = 5000;
    private UdpSocket server = new UdpSocket();
    public Movement movement_;



    private void Awake()
    {

    }
    void Start()
    {
        server.Start(sIP, sPort, "test", verbose: true);
        Debug.Log("server started");
    }

    void Update()
    {
    }

    public void LoadJson()
    {
        StreamReader r = new StreamReader("file.json");

        string json = r.ReadToEnd();
        List<Movement> movements = JsonConvert.DeserializeObject<List<Movement>>(json);
    }
}




public class Movement
{
    public int move_forward;
    public int move_backwards;
    public int rotate_left;
    public int rotate_right;
}