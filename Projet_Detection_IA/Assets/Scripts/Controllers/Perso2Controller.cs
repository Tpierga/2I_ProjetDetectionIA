using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Perso2Controller : MonoBehaviour
{
    public float speed = 10;
    
    private float timeToChangeDirection;
    public float gravity = 8;
    private Vector3 moveDirection = Vector3.zero;
    private Vector3 rotVector = Vector3.zero;
    private CharacterController Claude;
    private Animator anim;
    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        Claude = GetComponent<CharacterController>();
    }

    // Update is called once per frame
    void Update()
    {
        DirigerPerso();   
    }
    void DirigerPerso()
    {
        if (Claude.isGrounded)
        {
            if (Input.GetKeyDown("[5]"))
            {
                anim.SetBool("walk", true);
                Debug.Log("Claude avance");
                moveDirection = new Vector3(0, 0, Input.GetAxis("Vertical"));
                moveDirection *= speed;
                moveDirection = transform.TransformDirection(moveDirection);


            }
            else if (Input.GetKeyUp("[5]"))
            {
                anim.SetBool("walk", false);
                moveDirection = new Vector3(0, 0, 0);
                Debug.Log("Kevin ne se meut plus");
            }
            else if (Input.GetKeyDown("[2]"))
            {
                anim.SetBool("walk", false);
                anim.SetBool("backwards", true);
                moveDirection = new Vector3(0, 0, Input.GetAxis("Vertical"));
                moveDirection *= speed;
                moveDirection = transform.TransformDirection(moveDirection);

            }
            else if (Input.GetKeyUp("[2]"))
            {
                anim.SetBool("walk", false);
                anim.SetBool("backwards", false);
                moveDirection = new Vector3(0, 0, 0);

            }
            else if (Input.GetKeyDown("[1]"))
            {
                rotVector = -Vector3.up;
            }
            else if (Input.GetKeyUp("[1]"))
            {
                rotVector = new Vector3(0, 0, 0);
            }
            else if (Input.GetKeyDown("[3]"))
            {
                rotVector = Vector3.up;
            }
            else if (Input.GetKeyUp("[3]"))
            {
                rotVector = new Vector3(0, 0, 0);
            }

        }
        moveDirection.y -= gravity * Time.deltaTime;
        transform.Rotate(rotVector * Time.deltaTime * speed * 10);
        Claude.Move(moveDirection * Time.deltaTime);
    }
}
