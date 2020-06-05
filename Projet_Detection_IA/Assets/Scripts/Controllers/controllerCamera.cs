using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class controllerCamera : MonoBehaviour
{
    // Start is called before the first frame update
    public GameObject camRobot;
    
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Rotate(); 
    }
    
    void Rotate()
    {
        if (Input.GetKey(KeyCode.L))
        {
            transform.Rotate(-Vector3.up);
        }
        else if (Input.GetKey(KeyCode.M))
        {
            transform.Rotate(Vector3.up);
        }
    }
}
