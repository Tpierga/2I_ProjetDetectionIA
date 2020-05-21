﻿using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using ConsoleApplication1;
using UnityEngine;

public class controllerOmni : MonoBehaviour
{
    public GameObject robot;
    public float rotationSpeed = 10;
    Vector3 currentEulerAngles;
    float x;
    float y;
    float z;

    public string sIP = "127.0.0.1";
    public int sPort = 50000;

    private UdpSocket server = new UdpSocket();
    private int _t = 0;

    public SnapShotCamera snapCam;
    // Start is called before the first frame update
    //Initialisation de nos variables pour le raycast
    //rayDistance est la distance à laquelle le rayon détecte un objet
    [SerializeField] private float rayDistance;
    //vecteur_correction élève le rayon au-dessus du sol et le centre pour qu'il parte du centre du robot
    private Vector3 vecteur_correction = new Vector3(-0.7f, 0.5f, 0);
    [SerializeField] private LayerMask layers;



    void Start()
    {
        server.Start(sIP, sPort, "test", verbose: true);
        Debug.Log("server started");
        
    }
    
    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            snapCam.TakeSnapShot();
            Debug.Log("snapshot Taken");
        }
        Forward();
        Rotate();
        Sensors();
    }
    
    private void LateUpdate()
    {
        var bytes = snapCam.EncodeImage();
        if (bytes != null && bytes.Length > 0)
        {
            server.SendImageTo("127.0.0.1", 28000, bytes);
        }
    }
    
    void Forward()
    {
        if (Input.GetKey(KeyCode.W))
        {
            transform.Translate(Vector3.forward * ((Time.deltaTime) * 2));
            if (Input.GetKey(KeyCode.Q))
            {
                transform.Rotate(-Vector3.up);
            }
            else if (Input.GetKey(KeyCode.D))
            {
                transform.Rotate(Vector3.up);
            }
        }
        else if (Input.GetKey(KeyCode.S))
        {
            transform.Translate(-Vector3.forward * ((Time.deltaTime) * 2));
            if (Input.GetKey(KeyCode.Q))
            {
                transform.Rotate(-Vector3.up);
            }
            else if (Input.GetKey(KeyCode.D))
            {
                transform.Rotate(Vector3.up);
            }
        } 
    }

    void Rotate()
    {
        if (Input.GetKey(KeyCode.Q))
        {
            transform.Rotate(-Vector3.up*rotationSpeed*Time.deltaTime);
            //modifying the Vector3, based on input multiplied by speed and time
            
        }
        else if (Input.GetKey(KeyCode.D))
        {
            transform.Rotate(Vector3.up*rotationSpeed*Time.deltaTime);
            //modifying the Vector3, based on input multiplied by speed and time
          
        }
    }
    
    void Sensors()
    {
        RaycastHit hit1;
        RaycastHit hit2;
        RaycastHit hit3;
        RaycastHit hit4;
        
        //Vector3 offset2 = new Vector3(1.4f, 0, 0);
        //Vector3 offset4 = new Vector3(0, 0, 0);
        //Vector3 offset3 = new Vector3(1.4f, 0, 0);
        
        // Directions des raycast : bleu et rouge > direction 1
        // Vert : direction 3 - Jaune : direction 4
        var direction1 = transform.TransformDirection(Vector3.forward) * rayDistance;
        var direction3 = transform.TransformDirection(Vector3.left) * rayDistance;
        var direction4 = transform.TransformDirection(Vector3.right) * rayDistance;
        //Origines des rayons
        Vector3 origine1 = transform.position + transform.up * 0.5f + transform.forward * 0.1f;
        Vector3 origine2 = transform.position - transform.right * 1.5f + transform.up * 0.5f + transform.forward * 0.1f;
        Vector3 origine3 = transform.position - transform.right * 1.5f + transform.up * 0.5f;
        Vector3 origine4 = transform.position + transform.up * 0.5f;
        //Affichage des rayons
        Debug.DrawRay(origine1, direction1, Color.red);
        Debug.DrawRay(origine2, direction1, Color.blue);
        Debug.DrawRay(origine3, direction3, Color.green);
        Debug.DrawRay(origine4, direction4, Color.yellow);
        //Détection d'objets pour chaque rayon
        // Physics.Raycast renvoie un booléen True si le rayon touche quelque chose
        //rayon rouge
        bool touche1 = Physics.Raycast(origine1, direction1, out hit1, rayDistance, layers);
        //rayon bleu
        bool touche2=Physics.Raycast(origine2, direction1, out hit2, rayDistance, layers);
        //rayon vert
        bool touche3 = Physics.Raycast(origine3, direction3, out hit3, rayDistance, layers);
        //rayon jaune
        bool touche4 = Physics.Raycast(origine4, direction4, out hit4, rayDistance, layers);
        if (touche1)
        {

            Debug.Log("aie rouge");
            //transform.Rotate(-Vector3.up);

        }
        if (touche2)
        {

            Debug.Log("aie bleu");
           // transform.Rotate(-Vector3.up);

        }
        if (touche3)
        {

           Debug.Log("aie vert");
        //    transform.Rotate(-Vector3.up);

        }
        if (touche4)
        {

            Debug.Log("aie jaune");
            //transform.Rotate(-Vector3.up);

        }
    }

}
