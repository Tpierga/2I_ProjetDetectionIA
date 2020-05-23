using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterController : MonoBehaviour
{
    private float horizontalInput;
    public float speed = 40;
    private Animator Anim;
    private CharacterController Frank;
    private float timeToChangeDirection;
    // Start is called before the first frame update
    void Start()
    {
        Anim = GetComponent<Animator>();
        Frank = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        
        Diriger();
        

    }
    private void Diriger()
    {
        //float angle = Random.Range(0f, 360f);
        //Quaternion quat = Quaternion.AngleAxis(angle, Vector3.up);
        //Vector3 newRotation = quat * Vector3.left;
        //transform.Rotate(newRotation);
        //timeToChangeDirection = Random.Range(1f, 4f);
        //Debug.Log(timeToChangeDirection);
        
        if (Input.GetKeyDown("up"))
        {
            Anim.SetBool("walk", true);
            Debug.Log("Kevin avance");
        }
        else if (Input.GetKeyUp("up"))
        { 
            Anim.SetBool("walk", false);
            
            Debug.Log("Kevin ne se meut plus");
        }
        else if (Input.GetKeyDown("down"))
        {
            Anim.SetBool("walk", false);
            Anim.SetBool("backwards", true);


        }
        else if (Input.GetKeyUp("down"))
        {
            Anim.SetBool("walk", false);
            Anim.SetBool("backwards", false);

        }
        horizontalInput = Input.GetAxis("Horizontal");
        // Pour le faire tourner
        transform.Rotate(Vector3.up, Time.deltaTime * speed * horizontalInput);

    }
}
