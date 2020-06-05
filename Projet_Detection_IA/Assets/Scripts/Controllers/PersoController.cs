using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PersoController : MonoBehaviour
{
    
    public float speed = 10;
    
    
    private float timeToChangeDirection;
    public float gravity = 8;
    private Vector3 moveDirection = Vector3.zero;
    private CharacterController Cc;
    private Animator anim;
    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        Cc = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        
        DirigerPerso();
       
     
    }
    
    void DirigerPerso ()
    {
        if (Cc.isGrounded)
        {
            if (Input.GetKeyDown("up"))
            {
                anim.SetBool("walk", true);
                Debug.Log("Kevin avance");
                moveDirection = new Vector3(0, 0, Input.GetAxis("Vertical"));
                moveDirection *= speed;
                moveDirection = transform.TransformDirection(moveDirection);
                
                
            }
            else if (Input.GetKeyUp("up"))
            {
                anim.SetBool("walk", false);
                moveDirection = new Vector3(0, 0, 0);
                Debug.Log("Kevin ne se meut plus");
            }
            else if (Input.GetKeyDown("down"))
            {
                anim.SetBool("walk", false);
                anim.SetBool("backwards", true);
                moveDirection = new Vector3(0, 0, Input.GetAxis("Vertical"));
                moveDirection *= speed;
                moveDirection = transform.TransformDirection(moveDirection);
             
            }
            else if (Input.GetKeyUp("down"))
            {
                anim.SetBool("walk", false);
                anim.SetBool("backwards", false);
                moveDirection = new Vector3(0, 0, 0);

            }
        }
        moveDirection.y -= gravity * Time.deltaTime;
        transform.Rotate(Vector3.up * Input.GetAxis("Horizontal") * Time.deltaTime * speed * 10);
        Cc.Move(moveDirection * Time.deltaTime);
    }
}
